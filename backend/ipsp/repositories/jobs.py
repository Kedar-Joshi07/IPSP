"""Synchronous persistence operations for job metadata and guarded transitions."""

from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import datetime
from typing import Any

from sqlalchemy import Result, Select, func, select, update
from sqlalchemy.orm import Session

from ipsp.database.models import JobRecord
from ipsp.jobs.contracts import JobError, JobProgress, JobSnapshot
from ipsp.jobs.enums import JobStatus, JobType
from ipsp.security.redaction import sanitize_structured_data


def _updated_one(result: Result[Any]) -> bool:
    return int(getattr(result, "rowcount", 0)) == 1


def decode_artifact_references(value: str) -> tuple[str, ...]:
    """Decode only valid persisted string references without Python object reconstruction."""
    try:
        decoded = json.loads(value)
    except (TypeError, ValueError):
        return ()
    if not isinstance(decoded, list) or not all(isinstance(item, str) for item in decoded):
        return ()
    return tuple(decoded)


def snapshot_from_record(record: JobRecord) -> JobSnapshot:
    """Detach an immutable contract from a live ORM record."""
    error = None
    if record.error_code is not None and record.error_message is not None:
        error = JobError(record.error_code, record.error_message, record.retryable)
    return JobSnapshot(
        job_id=record.job_id,
        job_type=JobType(record.job_type),
        status=JobStatus(record.status),
        progress=JobProgress(
            percent=record.progress_percent,
            phase=record.progress_phase,
            message=record.progress_message,
        ),
        trace_id=record.trace_id,
        owner_user_id=record.owner_user_id,
        request_id=record.request_id,
        attempt_count=record.attempt_count,
        max_attempts=record.max_attempts,
        retryable=record.retryable,
        cancel_requested=record.cancel_requested,
        artifact_refs=decode_artifact_references(record.artifact_refs_json),
        created_at=record.created_at,
        queued_at=record.queued_at,
        started_at=record.started_at,
        finished_at=record.finished_at,
        updated_at=record.updated_at,
        error=error,
    )


class JobRepository:
    """Own job SQL while callers retain transaction and commit responsibility."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, record: JobRecord) -> None:
        self._session.add(record)

    def get_by_job_id(self, job_id: str) -> JobRecord | None:
        return self._session.scalar(select(JobRecord).where(JobRecord.job_id == job_id))

    def get_for_owner(self, job_id: str, owner_user_id: int) -> JobRecord | None:
        return self._session.scalar(
            select(JobRecord).where(
                JobRecord.job_id == job_id,
                JobRecord.owner_user_id == owner_user_id,
            )
        )

    def list_for_owner(self, owner_user_id: int, *, limit: int, offset: int) -> list[JobRecord]:
        statement = (
            select(JobRecord)
            .where(JobRecord.owner_user_id == owner_user_id)
            .order_by(JobRecord.created_at.desc(), JobRecord.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self._session.scalars(statement))

    def list_by_status(self, status: JobStatus) -> list[JobRecord]:
        return list(self._session.scalars(self._status_statement(status)))

    def list_queued_for_types(self, job_types: Iterable[JobType]) -> list[JobRecord]:
        values = tuple(item.value for item in job_types)
        if not values:
            return []
        statement = self._status_statement(JobStatus.QUEUED).where(JobRecord.job_type.in_(values))
        return list(self._session.scalars(statement))

    def count_by_status(self, status: JobStatus) -> int:
        count = self._session.scalar(
            select(func.count()).select_from(JobRecord).where(JobRecord.status == status.value)
        )
        return int(count or 0)

    def mark_running(self, job_id: str, now: datetime) -> bool:
        result = self._session.execute(
            update(JobRecord)
            .where(JobRecord.job_id == job_id, JobRecord.status == JobStatus.QUEUED.value)
            .values(status=JobStatus.RUNNING.value, started_at=now, updated_at=now)
        )
        return _updated_one(result)

    def update_progress(self, job_id: str, progress: JobProgress, now: datetime) -> bool:
        result = self._session.execute(
            update(JobRecord)
            .where(
                JobRecord.job_id == job_id,
                JobRecord.status == JobStatus.RUNNING.value,
                JobRecord.cancel_requested.is_(False),
            )
            .values(
                progress_percent=progress.percent,
                progress_phase=progress.phase,
                progress_message=progress.message,
                updated_at=now,
            )
        )
        return _updated_one(result)

    def request_cancel(self, job_id: str, now: datetime) -> tuple[JobStatus, bool] | None:
        queued = self._session.execute(
            update(JobRecord)
            .where(JobRecord.job_id == job_id, JobRecord.status == JobStatus.QUEUED.value)
            .values(
                status=JobStatus.CANCELLED.value,
                cancel_requested=True,
                progress_phase="cancelled",
                progress_message="Cancelled.",
                finished_at=now,
                updated_at=now,
            )
        )
        if _updated_one(queued):
            return JobStatus.CANCELLED, True
        running = self._session.execute(
            update(JobRecord)
            .where(
                JobRecord.job_id == job_id,
                JobRecord.status == JobStatus.RUNNING.value,
                JobRecord.cancel_requested.is_(False),
            )
            .values(cancel_requested=True, updated_at=now)
        )
        if _updated_one(running):
            return JobStatus.RUNNING, True
        record = self.get_by_job_id(job_id)
        if (
            record is not None
            and record.status == JobStatus.RUNNING.value
            and record.cancel_requested
        ):
            return JobStatus.RUNNING, False
        return None

    def is_cancel_requested(self, job_id: str) -> bool:
        value = self._session.scalar(
            select(JobRecord.cancel_requested).where(
                JobRecord.job_id == job_id,
                JobRecord.status == JobStatus.RUNNING.value,
            )
        )
        return bool(value)

    def mark_succeeded(self, job_id: str, now: datetime) -> bool:
        result = self._session.execute(
            update(JobRecord)
            .where(
                JobRecord.job_id == job_id,
                JobRecord.status == JobStatus.RUNNING.value,
                JobRecord.cancel_requested.is_(False),
            )
            .values(
                status=JobStatus.SUCCEEDED.value,
                progress_percent=100,
                progress_phase="completed",
                progress_message="Completed.",
                finished_at=now,
                updated_at=now,
            )
        )
        return _updated_one(result)

    def mark_failed(
        self,
        job_id: str,
        error: JobError,
        now: datetime,
        *,
        allow_queued: bool = False,
    ) -> bool:
        statuses = [JobStatus.RUNNING.value]
        if allow_queued:
            statuses.append(JobStatus.QUEUED.value)
        result = self._session.execute(
            update(JobRecord)
            .where(JobRecord.job_id == job_id, JobRecord.status.in_(statuses))
            .values(
                status=JobStatus.FAILED.value,
                retryable=error.retryable,
                error_code=error.error_code,
                error_message=error.message,
                finished_at=now,
                updated_at=now,
            )
        )
        return _updated_one(result)

    def mark_cancelled(self, job_id: str, now: datetime) -> bool:
        result = self._session.execute(
            update(JobRecord)
            .where(
                JobRecord.job_id == job_id,
                JobRecord.status == JobStatus.RUNNING.value,
                JobRecord.cancel_requested.is_(True),
            )
            .values(
                status=JobStatus.CANCELLED.value,
                progress_phase="cancelled",
                progress_message="Cancelled.",
                finished_at=now,
                updated_at=now,
            )
        )
        return _updated_one(result)

    def prepare_retry(self, job_id: str, now: datetime) -> bool:
        result = self._session.execute(
            update(JobRecord)
            .where(
                JobRecord.job_id == job_id,
                JobRecord.status.in_([JobStatus.FAILED.value, JobStatus.CANCELLED.value]),
                JobRecord.retryable.is_(True),
                JobRecord.attempt_count < JobRecord.max_attempts,
            )
            .values(
                status=JobStatus.QUEUED.value,
                progress_percent=0,
                progress_phase="queued",
                progress_message="Queued.",
                attempt_count=JobRecord.attempt_count + 1,
                cancel_requested=False,
                error_code=None,
                error_message=None,
                queued_at=now,
                started_at=None,
                finished_at=None,
                updated_at=now,
            )
        )
        return _updated_one(result)

    def add_artifact_reference(self, job_id: str, reference: str, now: datetime) -> bool:
        record = self.get_by_job_id(job_id)
        if record is None or record.status != JobStatus.RUNNING.value:
            return False
        references = list(decode_artifact_references(record.artifact_refs_json))
        if reference not in references:
            references.append(reference)
        encoded = json.dumps(references, ensure_ascii=False, separators=(",", ":"))
        if len(encoded) > 16384:
            raise ValueError("Artifact references exceed the storage limit")
        result = self._session.execute(
            update(JobRecord)
            .where(
                JobRecord.job_id == job_id,
                JobRecord.status == JobStatus.RUNNING.value,
                JobRecord.cancel_requested.is_(False),
            )
            .values(artifact_refs_json=encoded, updated_at=now)
        )
        return _updated_one(result)

    @staticmethod
    def encode_metadata(metadata: object) -> str:
        value = json.dumps(
            sanitize_structured_data(metadata),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        if len(value) > 16384:
            raise ValueError("Job metadata exceeds the storage limit")
        return value

    @staticmethod
    def _status_statement(status: JobStatus) -> Select[tuple[JobRecord]]:
        return select(JobRecord).where(JobRecord.status == status.value).order_by(JobRecord.id)
