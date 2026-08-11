"""Typed job interfaces with no worker or queue implementation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from ipsp.jobs.enums import JobStatus, JobType


@dataclass(frozen=True, slots=True)
class JobProgress:
    """Sanitized progress snapshot suitable for persistence or API mapping."""

    percent: int
    phase: str
    message: str

    def __post_init__(self) -> None:
        if not 0 <= self.percent <= 100:
            raise ValueError("Job progress percent must be between 0 and 100")


@dataclass(frozen=True, slots=True)
class JobError:
    """Safe job failure contract without raw exception or stack details."""

    error_code: str
    message: str
    retryable: bool


@dataclass(frozen=True, slots=True)
class JobSnapshot:
    """Current immutable view of job metadata."""

    job_id: str
    job_type: JobType
    status: JobStatus
    progress: JobProgress
    trace_id: str
    owner_id: str | None
    created_at: datetime
    updated_at: datetime
    error: JobError | None = None


class JobBackend(Protocol):
    """Execution-backend boundary for future local or distributed workers."""

    def submit(self, job_id: str, job_type: JobType) -> None: ...

    def cancel(self, job_id: str) -> bool: ...

    def retry(self, job_id: str) -> bool: ...


class JobRepository(Protocol):
    """Persistence boundary; the SQLite implementation arrives with database work."""

    def get(self, job_id: str) -> JobSnapshot | None: ...

    def save(self, job: JobSnapshot) -> None: ...


class JobService(Protocol):
    """Application boundary for progress, cancellation, and retry operations."""

    def progress(self, job_id: str) -> JobProgress: ...

    def cancel(self, job_id: str) -> bool: ...

    def retry(self, job_id: str) -> bool: ...
