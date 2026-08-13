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
    error_code: str | None = None
    checks: dict[str, str] = Field(default_factory=dict)
    deferred_checks: list[str] = Field(default_factory=list)


class LivenessResponse(BaseModel):
    """Process-only infrastructure response with no dependency fields."""

    status: Literal["alive"] = "alive"
    timestamp_utc: datetime


class BrowserConfigResponse(BaseModel):
    """Public, non-secret browser bootstrap configuration."""

    default_theme: Literal["system", "dark", "light"]
    csrf_cookie_name: str
    csrf_header_name: str


class ApiInfoResponse(BaseModel):
    """Versioned API-root metadata without business or simulation output."""

    name: str
    version: str
    status: Literal["foundation"] = "foundation"
    browser: BrowserConfigResponse
