"""Common API response contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Stable safe error envelope returned by every central error handler."""

    error_code: str
    message: str
    trace_id: str
    recoverable: bool = False
    details: dict[str, Any] | list[dict[str, Any]] | None = None


class HealthResponse(BaseModel):
    """Minimal infrastructure-probe response."""

    status: Literal["alive", "ready", "not_ready"]
    timestamp_utc: datetime
    checks: dict[str, str] = Field(default_factory=dict)
    deferred_checks: list[str] = Field(default_factory=list)


class ApiInfoResponse(BaseModel):
    """Versioned API-root metadata without business or simulation output."""

    name: str
    version: str
    status: Literal["foundation"] = "foundation"
