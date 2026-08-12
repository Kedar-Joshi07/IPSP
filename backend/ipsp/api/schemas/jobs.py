"""Safe Pydantic response contracts for generic job management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ipsp.jobs.contracts import JobSnapshot
from ipsp.jobs.enums import JobStatus, JobType


class JobProgressResponse(BaseModel):
    percent: int = Field(ge=0, le=100)
    phase: str
    message: str


class JobErrorResponse(BaseModel):
    error_code: str
    message: str
    retryable: bool


class JobResponse(BaseModel):
    """Owner-safe job view excluding internal metadata and ORM state."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    job_type: JobType
    status: JobStatus
    progress: JobProgressResponse
    created_at: datetime
    queued_at: datetime
    updated_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    retryable: bool
    cancel_requested: bool
    attempt_count: int
    max_attempts: int
    error: JobErrorResponse | None
    artifact_refs: tuple[str, ...]

    @classmethod
    def from_snapshot(cls, snapshot: JobSnapshot) -> "JobResponse":
        return cls(
            job_id=snapshot.job_id,
            job_type=snapshot.job_type,
            status=snapshot.status,
            progress=JobProgressResponse(
                percent=snapshot.progress.percent,
                phase=snapshot.progress.phase,
                message=snapshot.progress.message,
            ),
            created_at=snapshot.created_at,
            queued_at=snapshot.queued_at,
            updated_at=snapshot.updated_at,
            started_at=snapshot.started_at,
            finished_at=snapshot.finished_at,
            retryable=snapshot.retryable,
            cancel_requested=snapshot.cancel_requested,
            attempt_count=snapshot.attempt_count,
            max_attempts=snapshot.max_attempts,
            error=(
                JobErrorResponse(
                    error_code=snapshot.error.error_code,
                    message=snapshot.error.message,
                    retryable=snapshot.error.retryable,
                )
                if snapshot.error is not None
                else None
            ),
            artifact_refs=snapshot.artifact_refs,
        )


class JobListResponse(BaseModel):
    jobs: list[JobResponse]
