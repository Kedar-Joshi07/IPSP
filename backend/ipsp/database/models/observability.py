"""Append-only durable audit and security event ORM entity."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import CheckConstraint, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ipsp.database.models.base import Base
from ipsp.database.types import UTCDateTime


class AuditEvent(Base):
    """Historical event envelope without destructive foreign-key coupling."""

    __tablename__ = "audit_events"
    __table_args__ = (
        CheckConstraint("duration_ms IS NULL OR duration_ms >= 0", name="duration_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[str] = mapped_column(String(36), nullable=False, unique=True, index=True)
    timestamp_utc: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, index=True)
    stream: Mapped[str] = mapped_column(String(32), nullable=False)
    trace_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    request_id: Mapped[str] = mapped_column(String(128), nullable=False)
    session_correlation_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    resolved_role: Mapped[str | None] = mapped_column(String(255), nullable=True)
    component: Mapped[str] = mapped_column(String(128), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    duration_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    error_code: Mapped[str | None] = mapped_column(String(128), nullable=True)
    resource_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    resource_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    project_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dataset_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dataset_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    semantic_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    capability_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_version_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    run_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    llm_provider: Mapped[str | None] = mapped_column(String(255), nullable=True)
    llm_model: Mapped[str | None] = mapped_column(String(255), nullable=True)
    llm_request_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, nullable=False)
