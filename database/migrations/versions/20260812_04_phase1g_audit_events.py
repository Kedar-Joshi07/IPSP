"""Add append-only durable audit and security events.

Revision ID: 20260812_04
Revises: 20260811_03
Create Date: 2026-08-12
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from ipsp.database.types import UTCDateTime

revision: str = "20260812_04"
down_revision: str | Sequence[str] | None = "20260811_03"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create only the durable audit event table."""
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=36), nullable=False),
        sa.Column("timestamp_utc", UTCDateTime(), nullable=False),
        sa.Column("stream", sa.String(length=32), nullable=False),
        sa.Column("trace_id", sa.String(length=128), nullable=False),
        sa.Column("request_id", sa.String(length=128), nullable=False),
        sa.Column("session_correlation_id", sa.String(length=128), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("resolved_role", sa.String(length=255), nullable=True),
        sa.Column("component", sa.String(length=128), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("duration_ms", sa.Float(), nullable=True),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("resource_type", sa.String(length=128), nullable=True),
        sa.Column("resource_id", sa.String(length=255), nullable=True),
        sa.Column("project_id", sa.String(length=255), nullable=True),
        sa.Column("dataset_id", sa.String(length=255), nullable=True),
        sa.Column("dataset_version_id", sa.String(length=255), nullable=True),
        sa.Column("semantic_version_id", sa.String(length=255), nullable=True),
        sa.Column("capability_version_id", sa.String(length=255), nullable=True),
        sa.Column("model_id", sa.String(length=255), nullable=True),
        sa.Column("model_version_id", sa.String(length=255), nullable=True),
        sa.Column("run_id", sa.String(length=255), nullable=True),
        sa.Column("llm_provider", sa.String(length=255), nullable=True),
        sa.Column("llm_model", sa.String(length=255), nullable=True),
        sa.Column("llm_request_id", sa.String(length=255), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "duration_ms IS NULL OR duration_ms >= 0",
            name=op.f("ck_audit_events_duration_nonnegative"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_events")),
    )
    op.create_index(op.f("ix_audit_events_action"), "audit_events", ["action"], unique=False)
    op.create_index(op.f("ix_audit_events_event_id"), "audit_events", ["event_id"], unique=True)
    op.create_index(
        op.f("ix_audit_events_timestamp_utc"), "audit_events", ["timestamp_utc"], unique=False
    )
    op.create_index(op.f("ix_audit_events_trace_id"), "audit_events", ["trace_id"], unique=False)
    op.create_index(op.f("ix_audit_events_user_id"), "audit_events", ["user_id"], unique=False)


def downgrade() -> None:
    """Remove only the durable audit event table."""
    op.drop_index(op.f("ix_audit_events_user_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_trace_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_timestamp_utc"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_event_id"), table_name="audit_events")
    op.drop_index(op.f("ix_audit_events_action"), table_name="audit_events")
    op.drop_table("audit_events")
