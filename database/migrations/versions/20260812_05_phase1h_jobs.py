"""Add persistent local job metadata.

Revision ID: 20260812_05
Revises: 20260812_04
Create Date: 2026-08-12
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from ipsp.database.types import UTCDateTime

revision: str = "20260812_05"
down_revision: str | Sequence[str] | None = "20260812_04"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_STATUSES = "'QUEUED','RUNNING','SUCCEEDED','FAILED','CANCELLED'"
_JOB_TYPES = (
    "'UPLOAD_PROCESSING','PROFILING','RELATIONSHIP_ANALYSIS','MODEL_TRAINING',"
    "'SYNTHETIC_FITTING','SIMULATION','REPORT_GENERATION','BACKUP','RESTORE'"
)


def upgrade() -> None:
    """Create only the persistent jobs table."""
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("job_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("progress_percent", sa.Integer(), nullable=False),
        sa.Column("progress_phase", sa.String(length=128), nullable=False),
        sa.Column("progress_message", sa.String(length=512), nullable=False),
        sa.Column("owner_user_id", sa.Integer(), nullable=True),
        sa.Column("trace_id", sa.String(length=128), nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("retryable", sa.Boolean(), nullable=False),
        sa.Column("cancel_requested", sa.Boolean(), nullable=False),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("error_message", sa.String(length=512), nullable=True),
        sa.Column("artifact_refs_json", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            UTCDateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("queued_at", UTCDateTime(), nullable=False),
        sa.Column("started_at", UTCDateTime(), nullable=True),
        sa.Column("finished_at", UTCDateTime(), nullable=True),
        sa.Column(
            "updated_at",
            UTCDateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "progress_percent >= 0 AND progress_percent <= 100",
            name=op.f("ck_jobs_progress_percent_range"),
        ),
        sa.CheckConstraint("attempt_count >= 1", name=op.f("ck_jobs_attempt_count_positive")),
        sa.CheckConstraint("max_attempts >= 1", name=op.f("ck_jobs_max_attempts_positive")),
        sa.CheckConstraint(
            "attempt_count <= max_attempts", name=op.f("ck_jobs_attempt_within_maximum")
        ),
        sa.CheckConstraint(f"status IN ({_STATUSES})", name=op.f("ck_jobs_status_allowed")),
        sa.CheckConstraint(f"job_type IN ({_JOB_TYPES})", name=op.f("ck_jobs_job_type_allowed")),
        sa.CheckConstraint(
            "length(progress_phase) <= 128", name=op.f("ck_jobs_progress_phase_bounded")
        ),
        sa.CheckConstraint(
            "length(progress_message) <= 512", name=op.f("ck_jobs_progress_message_bounded")
        ),
        sa.CheckConstraint(
            "length(artifact_refs_json) <= 16384", name=op.f("ck_jobs_artifact_refs_bounded")
        ),
        sa.CheckConstraint("length(metadata_json) <= 16384", name=op.f("ck_jobs_metadata_bounded")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_jobs")),
    )
    op.create_index(op.f("ix_jobs_job_id"), "jobs", ["job_id"], unique=True)
    op.create_index(op.f("ix_jobs_job_type"), "jobs", ["job_type"], unique=False)
    op.create_index(op.f("ix_jobs_status"), "jobs", ["status"], unique=False)
    op.create_index(
        "ix_jobs_owner_user_id_created_at",
        "jobs",
        ["owner_user_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    """Remove only the persistent jobs table."""
    op.drop_index("ix_jobs_owner_user_id_created_at", table_name="jobs")
    op.drop_index(op.f("ix_jobs_status"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_job_type"), table_name="jobs")
    op.drop_index(op.f("ix_jobs_job_id"), table_name="jobs")
    op.drop_table("jobs")
