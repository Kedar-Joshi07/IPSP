"""Persistent control-plane metadata for trusted background jobs."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from ipsp.database.models.base import Base
from ipsp.database.types import UTCDateTime, utc_now
from ipsp.jobs.enums import JobStatus, JobType

_STATUSES = ",".join(f"'{item.value}'" for item in JobStatus)
_JOB_TYPES = ",".join(f"'{item.value}'" for item in JobType)


class JobRecord(Base):
    """One logical job and its bounded manual execution-attempt state."""

    __tablename__ = "jobs"
    __table_args__ = (
        CheckConstraint(f"status IN ({_STATUSES})", name="status_allowed"),
        CheckConstraint(f"job_type IN ({_JOB_TYPES})", name="job_type_allowed"),
        CheckConstraint(
            "progress_percent >= 0 AND progress_percent <= 100",
            name="progress_percent_range",
        ),
        CheckConstraint("attempt_count >= 1", name="attempt_count_positive"),
        CheckConstraint("max_attempts >= 1", name="max_attempts_positive"),
        CheckConstraint("attempt_count <= max_attempts", name="attempt_within_maximum"),
        CheckConstraint("length(progress_phase) <= 128", name="progress_phase_bounded"),
        CheckConstraint("length(progress_message) <= 512", name="progress_message_bounded"),
        CheckConstraint("length(artifact_refs_json) <= 16384", name="artifact_refs_bounded"),
        CheckConstraint("length(metadata_json) <= 16384", name="metadata_bounded"),
        Index("ix_jobs_owner_user_id_created_at", "owner_user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, index=True)
    job_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    progress_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    progress_phase: Mapped[str] = mapped_column(String(128), nullable=False, default="queued")
    progress_message: Mapped[str] = mapped_column(String(512), nullable=False, default="Queued.")
    owner_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    trace_id: Mapped[str] = mapped_column(String(128), nullable=False)
    request_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    retryable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cancel_requested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    error_code: Mapped[str | None] = mapped_column(String(128), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(512), nullable=True)
    artifact_refs_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    metadata_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), nullable=False, default=utc_now, server_default=text("CURRENT_TIMESTAMP")
    )
    queued_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), nullable=False, default=utc_now, server_default=text("CURRENT_TIMESTAMP")
    )
