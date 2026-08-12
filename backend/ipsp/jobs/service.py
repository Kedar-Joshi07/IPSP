"""Application policy for persistent jobs and owner-scoped control actions."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import uuid4

from ipsp.database.models import JobRecord
from ipsp.database.session import DatabaseSessionFactory
from ipsp.errors.exceptions import IPSPError
from ipsp.jobs.contracts import JobBackend, JobError, JobProgress, JobSnapshot
from ipsp.jobs.enums import JobStatus, JobType
from ipsp.observability.audit import AuditService
from ipsp.observability.context import current_observability_context
from ipsp.observability.events import EventStream
from ipsp.repositories.jobs import JobRepository, snapshot_from_record

logger = logging.getLogger("ipsp.jobs")


def _not_found() -> IPSPError:
    return IPSPError("JOB-NOT-FOUND", "Job was not found.")


class JobService:
    """Persist jobs before scheduling and enforce owner-safe lifecycle policy."""

    def __init__(
        self,
        sessions: DatabaseSessionFactory,
        backend: JobBackend,
        audit: AuditService,
    ) -> None:
        self._sessions = sessions
        self._backend = backend
        self._audit = audit

    def submit(
        self,
        job_type: JobType,
        owner_user_id: int | None,
        *,
        retryable: bool = False,
        max_attempts: int = 1,
        metadata: object | None = None,
    ) -> JobSnapshot:
        """Create one trusted internal job and asynchronously schedule its persisted ID."""
        if not self._backend.can_handle(job_type):
            raise IPSPError("JOB-HANDLER-UNAVAILABLE", "Job handler is unavailable.")
        if not self._backend.health().accepting_jobs:
            raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
        if not 1 <= max_attempts <= 100:
            raise ValueError("Maximum attempts must be between 1 and 100")
        if owner_user_id is not None and owner_user_id <= 0:
            raise ValueError("Owner user ID must be positive")
        now = datetime.now(UTC)
        observability = current_observability_context()
        job_id = str(uuid4())
        trace_id = observability.trace_id or str(uuid4())
        request_id = observability.request_id or str(uuid4())
        with self._sessions.transaction() as session:
            repository = JobRepository(session)
            record = JobRecord(
                job_id=job_id,
                job_type=job_type.value,
                status=JobStatus.QUEUED.value,
                progress_percent=0,
                progress_phase="queued",
                progress_message="Queued.",
                owner_user_id=owner_user_id,
                trace_id=trace_id,
                request_id=request_id,
                attempt_count=1,
                max_attempts=max_attempts,
                retryable=retryable,
                cancel_requested=False,
                artifact_refs_json="[]",
                metadata_json=repository.encode_metadata(metadata or {}),
                created_at=now,
                queued_at=now,
                updated_at=now,
            )
            repository.add(record)
            self._audit.record_in_session(
                session,
                stream=EventStream.AUDIT,
                component="jobs",
                action="job.submit",
                status="success",
                severity="INFO",
                user_id=owner_user_id,
                resource_type="job",
                resource_id=job_id,
                trace_id=trace_id,
                request_id=request_id,
                metadata={"job_type": job_type.value, "status": JobStatus.QUEUED.value},
            )
        try:
            self._backend.enqueue(job_id)
        except Exception as exc:
            error = JobError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.", True)
            with self._sessions.transaction() as session:
                JobRepository(session).mark_failed(
                    job_id, error, datetime.now(UTC), allow_queued=True
                )
            if isinstance(exc, IPSPError):
                raise
            raise IPSPError(error.error_code, error.message, recoverable=True) from None
        logger.info(
            "Job submitted",
            extra={
                "ipsp_action": "job.submitted",
                "ipsp_stream": "application",
                "ipsp_component": "jobs",
                "ipsp_status": "success",
                "ipsp_resource_type": "job",
                "ipsp_resource_id": job_id,
                "ipsp_user_id": owner_user_id,
                "ipsp_trace_id": trace_id,
                "ipsp_request_id": request_id,
                "ipsp_metadata": {"job_type": job_type.value},
            },
        )
        return self.get_internal(job_id)

    def get(self, job_id: str, owner_user_id: int) -> JobSnapshot:
        with self._sessions.session() as session:
            record = JobRepository(session).get_for_owner(job_id, owner_user_id)
            if record is None:
                raise _not_found()
            return snapshot_from_record(record)

    def get_internal(self, job_id: str) -> JobSnapshot:
        with self._sessions.session() as session:
            record = JobRepository(session).get_by_job_id(job_id)
            if record is None:
                raise _not_found()
            return snapshot_from_record(record)

    def list(self, owner_user_id: int, *, limit: int = 50, offset: int = 0) -> list[JobSnapshot]:
        with self._sessions.session() as session:
            records = JobRepository(session).list_for_owner(
                owner_user_id, limit=limit, offset=offset
            )
            return [snapshot_from_record(record) for record in records]

    def progress(self, job_id: str, owner_user_id: int) -> JobProgress:
        return self.get(job_id, owner_user_id).progress

    def cancel(self, job_id: str, owner_user_id: int) -> JobSnapshot:
        now = datetime.now(UTC)
        changed = False
        with self._sessions.transaction() as session:
            repository = JobRepository(session)
            record = repository.get_for_owner(job_id, owner_user_id)
            if record is None:
                raise _not_found()
            result = repository.request_cancel(job_id, now)
            if result is None:
                raise IPSPError(
                    "JOB-CANCEL-NOT-ALLOWED",
                    "Job can no longer be cancelled.",
                )
            _, changed = result
            if changed:
                self._audit.record_in_session(
                    session,
                    stream=EventStream.AUDIT,
                    component="jobs",
                    action="job.cancel",
                    status="success",
                    severity="INFO",
                    user_id=owner_user_id,
                    resource_type="job",
                    resource_id=job_id,
                    metadata={"job_type": record.job_type, "status": result[0].value},
                )
        if changed:
            logger.info(
                "Job cancellation requested",
                extra={
                    "ipsp_action": "job.cancel_requested",
                    "ipsp_stream": "application",
                    "ipsp_component": "jobs",
                    "ipsp_status": "success",
                    "ipsp_resource_type": "job",
                    "ipsp_resource_id": job_id,
                    "ipsp_user_id": owner_user_id,
                },
            )
        return self.get(job_id, owner_user_id)

    def retry(self, job_id: str, owner_user_id: int) -> JobSnapshot:
        now = datetime.now(UTC)
        with self._sessions.transaction() as session:
            repository = JobRepository(session)
            record = repository.get_for_owner(job_id, owner_user_id)
            if record is None:
                raise _not_found()
            job_type = JobType(record.job_type)
            if not self._backend.can_handle(job_type):
                raise IPSPError("JOB-HANDLER-UNAVAILABLE", "Job handler is unavailable.")
            if not self._backend.health().accepting_jobs:
                raise IPSPError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.")
            if not repository.prepare_retry(job_id, now):
                raise IPSPError(
                    "JOB-RETRY-NOT-ALLOWED",
                    "Job cannot be retried.",
                )
            self._audit.record_in_session(
                session,
                stream=EventStream.AUDIT,
                component="jobs",
                action="job.retry",
                status="success",
                severity="INFO",
                user_id=owner_user_id,
                resource_type="job",
                resource_id=job_id,
                metadata={"job_type": record.job_type, "attempt": record.attempt_count + 1},
            )
        try:
            self._backend.enqueue(job_id)
        except Exception as exc:
            error = JobError("JOB-WORKER-UNAVAILABLE", "Job worker is unavailable.", True)
            with self._sessions.transaction() as session:
                JobRepository(session).mark_failed(
                    job_id, error, datetime.now(UTC), allow_queued=True
                )
            if isinstance(exc, IPSPError):
                raise
            raise IPSPError(error.error_code, error.message, recoverable=True) from None
        logger.info(
            "Job retry requested",
            extra={
                "ipsp_action": "job.retry_requested",
                "ipsp_stream": "application",
                "ipsp_component": "jobs",
                "ipsp_status": "success",
                "ipsp_resource_type": "job",
                "ipsp_resource_id": job_id,
                "ipsp_user_id": owner_user_id,
            },
        )
        return self.get(job_id, owner_user_id)
