"""Trusted handler execution with fresh sessions and observability context."""

from __future__ import annotations

import logging
import re
import threading
import time
from collections.abc import Mapping
from datetime import UTC, datetime
from types import MappingProxyType
from uuid import uuid4

from ipsp.database.session import DatabaseSessionFactory
from ipsp.jobs.contracts import JobError, JobHandler, JobProgress, JobSnapshot
from ipsp.jobs.enums import JobStatus, JobType
from ipsp.observability.audit import AuditService
from ipsp.observability.context import bind_observability_context
from ipsp.observability.events import EventStream
from ipsp.repositories.jobs import JobRepository, snapshot_from_record

logger = logging.getLogger("ipsp.jobs")
_ARTIFACT_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,254}$")


class JobCancellationAcknowledged(Exception):
    """Internal control flow used only for cooperative worker cancellation."""


class PersistentJobExecutionContext:
    """Handler-facing capabilities backed by fresh transaction-scoped sessions."""

    def __init__(
        self,
        sessions: DatabaseSessionFactory,
        *,
        job_id: str,
        job_type: JobType,
        attempt: int,
    ) -> None:
        self._sessions = sessions
        self._job_id = job_id
        self._job_type = job_type
        self._attempt = attempt

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def job_type(self) -> JobType:
        return self._job_type

    @property
    def attempt(self) -> int:
        return self._attempt

    def update_progress(self, progress: JobProgress) -> None:
        with self._sessions.transaction() as session:
            updated = JobRepository(session).update_progress(
                self._job_id, progress, datetime.now(UTC)
            )
        if not updated:
            raise JobCancellationAcknowledged()
        logger.info(
            "Job progress updated",
            extra={
                "ipsp_action": "job.progress",
                "ipsp_stream": "performance",
                "ipsp_component": "jobs",
                "ipsp_status": "success",
                "ipsp_metadata": {"percent": progress.percent, "phase": progress.phase},
            },
        )

    def is_cancel_requested(self) -> bool:
        with self._sessions.session() as session:
            return JobRepository(session).is_cancel_requested(self._job_id)

    def raise_if_cancelled(self) -> None:
        if self.is_cancel_requested():
            raise JobCancellationAcknowledged()

    def add_artifact_reference(self, reference: str) -> None:
        if (
            not _ARTIFACT_REFERENCE.fullmatch(reference)
            or reference.startswith(("/", "\\"))
            or ".." in reference.split("/")
        ):
            raise ValueError("Artifact reference must be a safe relative identifier")
        with self._sessions.transaction() as session:
            updated = JobRepository(session).add_artifact_reference(
                self._job_id, reference, datetime.now(UTC)
            )
        if not updated:
            raise JobCancellationAcknowledged()


class JobExecutor:
    """Claim persisted work, execute registered code, and persist safe outcomes."""

    def __init__(
        self,
        sessions: DatabaseSessionFactory,
        audit: AuditService,
        handlers: Mapping[JobType, JobHandler] | None = None,
    ) -> None:
        self._sessions = sessions
        self._audit = audit
        self._handlers = MappingProxyType(dict(handlers or {}))
        self._shutdown_requested = threading.Event()

    @property
    def registered_types(self) -> frozenset[JobType]:
        return frozenset(self._handlers)

    def can_handle(self, job_type: JobType) -> bool:
        return job_type in self._handlers

    def prepare_start(self) -> None:
        """Allow executions for a newly started local worker lifecycle."""
        self._shutdown_requested.clear()

    def begin_shutdown(self) -> None:
        """Prevent a still-running handler from being reported as newly succeeded."""
        self._shutdown_requested.set()

    def recover_interrupted(self) -> tuple[str, ...]:
        """Fail prior-process RUNNING work and return safe QUEUED work eligible to enqueue."""
        with self._sessions.session() as session:
            running_jobs = [
                snapshot_from_record(record)
                for record in JobRepository(session).list_by_status(JobStatus.RUNNING)
            ]
        for snapshot in running_jobs:
            request_id = snapshot.request_id or str(uuid4())
            with bind_observability_context(
                trace_id=snapshot.trace_id,
                request_id=request_id,
                user_id=snapshot.owner_user_id,
                resource_type="job",
                resource_id=snapshot.job_id,
            ):
                with self._sessions.transaction() as session:
                    repository = JobRepository(session)
                    record = repository.get_by_job_id(snapshot.job_id)
                    if record is None:
                        continue
                    error = JobError(
                        "JOB-WORKER-INTERRUPTED",
                        "Job execution was interrupted.",
                        True,
                    )
                    if not repository.mark_failed(snapshot.job_id, error, datetime.now(UTC)):
                        continue
                    self._audit.record_in_session(
                        session,
                        stream=EventStream.AUDIT,
                        component="jobs",
                        action="job.recovered_interrupted",
                        status="failure",
                        severity="WARNING",
                        error_code=error.error_code,
                        metadata={"job_type": record.job_type},
                    )
                logger.warning(
                    "Interrupted job recovered",
                    extra={
                        "ipsp_action": "job.recovered_interrupted",
                        "ipsp_stream": "errors",
                        "ipsp_component": "jobs",
                        "ipsp_status": "failure",
                        "ipsp_error_code": "JOB-WORKER-INTERRUPTED",
                    },
                )
        with self._sessions.session() as session:
            queued = JobRepository(session).list_queued_for_types(self.registered_types)
            return tuple(record.job_id for record in queued)

    def execute(self, job_id: str) -> None:
        with self._sessions.transaction() as session:
            repository = JobRepository(session)
            record = repository.get_by_job_id(job_id)
            if record is None or record.status != JobStatus.QUEUED.value:
                return
            snapshot = snapshot_from_record(record)
            if not repository.mark_running(job_id, datetime.now(UTC)):
                return
        handler = self._handlers.get(snapshot.job_type)
        if handler is None:
            self._fail_without_exception(
                snapshot.job_id,
                JobError("JOB-HANDLER-UNAVAILABLE", "Job handler is unavailable.", True),
            )
            return
        request_id = snapshot.request_id or str(uuid4())
        with bind_observability_context(
            trace_id=snapshot.trace_id,
            request_id=request_id,
            user_id=snapshot.owner_user_id,
            resource_type="job",
            resource_id=job_id,
        ):
            self._run_handler(snapshot, handler)

    def _run_handler(self, snapshot: JobSnapshot, handler: JobHandler) -> None:
        job_id = snapshot.job_id
        started = time.perf_counter()
        logger.info(
            "Job execution started",
            extra={
                "ipsp_action": "job.started",
                "ipsp_stream": "application",
                "ipsp_component": "jobs",
                "ipsp_status": "success",
            },
        )
        context = PersistentJobExecutionContext(
            self._sessions,
            job_id=job_id,
            job_type=snapshot.job_type,
            attempt=snapshot.attempt_count,
        )
        try:
            context.raise_if_cancelled()
            handler(context)
            context.raise_if_cancelled()
        except JobCancellationAcknowledged:
            self._mark_cancelled(job_id, started)
        except Exception:
            if self._shutdown_requested.is_set():
                return
            logger.exception(
                "Job execution failed",
                extra={
                    "ipsp_action": "job.failed",
                    "ipsp_stream": "errors",
                    "ipsp_component": "jobs",
                    "ipsp_status": "failure",
                    "ipsp_error_code": "JOB-EXECUTION-FAILED",
                    "ipsp_duration_ms": round((time.perf_counter() - started) * 1000, 3),
                },
            )
            self._fail_without_exception(
                job_id,
                JobError("JOB-EXECUTION-FAILED", "Job execution failed.", snapshot.retryable),
            )
        else:
            if self._shutdown_requested.is_set():
                return
            with self._sessions.transaction() as session:
                succeeded = JobRepository(session).mark_succeeded(job_id, datetime.now(UTC))
            if succeeded:
                logger.info(
                    "Job execution succeeded",
                    extra={
                        "ipsp_action": "job.succeeded",
                        "ipsp_stream": "application",
                        "ipsp_component": "jobs",
                        "ipsp_status": "success",
                        "ipsp_duration_ms": round((time.perf_counter() - started) * 1000, 3),
                    },
                )
            else:
                self._mark_cancelled(job_id, started)

    def _mark_cancelled(self, job_id: str, started: float) -> None:
        with self._sessions.transaction() as session:
            cancelled = JobRepository(session).mark_cancelled(job_id, datetime.now(UTC))
        if cancelled:
            logger.info(
                "Job execution cancelled",
                extra={
                    "ipsp_action": "job.cancelled",
                    "ipsp_stream": "application",
                    "ipsp_component": "jobs",
                    "ipsp_status": "success",
                    "ipsp_duration_ms": round((time.perf_counter() - started) * 1000, 3),
                },
            )

    def _fail_without_exception(self, job_id: str, error: JobError) -> None:
        with self._sessions.transaction() as session:
            JobRepository(session).mark_failed(job_id, error, datetime.now(UTC), allow_queued=True)
