"""Canonical immutable contracts for persistent background jobs."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, TypeAlias

from ipsp.jobs.enums import JobStatus, JobType

_JOB_ERROR_CODE = re.compile(r"^JOB-[A-Z0-9_]+(?:-[A-Z0-9_]+)*$")


@dataclass(frozen=True, slots=True)
class JobProgress:
    """Sanitized progress snapshot suitable for persistence or API mapping."""

    percent: int
    phase: str
    message: str

    def __post_init__(self) -> None:
        if not 0 <= self.percent <= 100:
            raise ValueError("Job progress percent must be between 0 and 100")
        _validate_single_line("phase", self.phase, 128)
        _validate_single_line("message", self.message, 512)


@dataclass(frozen=True, slots=True)
class JobError:
    """Safe job failure contract without raw exception or stack details."""

    error_code: str
    message: str
    retryable: bool

    def __post_init__(self) -> None:
        if not _JOB_ERROR_CODE.fullmatch(self.error_code):
            raise ValueError("Job error code must use the JOB-* taxonomy")
        _validate_single_line("message", self.message, 512)


@dataclass(frozen=True, slots=True)
class JobSnapshot:
    """Current immutable view of job metadata."""

    job_id: str
    job_type: JobType
    status: JobStatus
    progress: JobProgress
    trace_id: str
    owner_user_id: int | None
    request_id: str | None
    attempt_count: int
    max_attempts: int
    retryable: bool
    cancel_requested: bool
    artifact_refs: tuple[str, ...]
    created_at: datetime
    queued_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    updated_at: datetime
    error: JobError | None = None


class JobBackend(Protocol):
    """Execution-backend boundary for local and future provider implementations."""

    def enqueue(self, job_id: str) -> None: ...

    def can_handle(self, job_type: JobType) -> bool: ...

    def start(self) -> None: ...

    def shutdown(self) -> None: ...

    def health(self) -> JobBackendHealth: ...


@dataclass(frozen=True, slots=True)
class JobBackendHealth:
    """Sanitized local worker state for readiness and future diagnostics."""

    running: bool
    accepting_jobs: bool
    worker_count: int
    queue_depth: int


class JobExecutionContext(Protocol):
    """Narrow trusted capability surface supplied to registered job handlers."""

    @property
    def job_id(self) -> str: ...

    @property
    def job_type(self) -> JobType: ...

    @property
    def attempt(self) -> int: ...

    def update_progress(self, progress: JobProgress) -> None: ...

    def is_cancel_requested(self) -> bool: ...

    def raise_if_cancelled(self) -> None: ...

    def add_artifact_reference(self, reference: str) -> None: ...


JobHandler: TypeAlias = Callable[[JobExecutionContext], None]


def _validate_single_line(name: str, value: str, maximum: int) -> None:
    if not value or len(value) > maximum or "\n" in value or "\r" in value:
        raise ValueError(f"Job {name} must be a bounded single-line string")
