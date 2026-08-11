"""Unversioned infrastructure probe routes."""

from datetime import UTC, datetime

from fastapi import APIRouter, Request

from ipsp.api.schemas.common import HealthResponse
from ipsp.services.readiness import ReadinessService

router = APIRouter(tags=["health"])


@router.get("/health/live", response_model=HealthResponse)
def liveness() -> HealthResponse:
    """Confirm only that the process and application router are alive."""
    return HealthResponse(status="alive", timestamp_utc=datetime.now(UTC))


@router.get("/health/ready", response_model=HealthResponse)
def readiness(request: Request) -> HealthResponse:
    """Report implemented checks and name later dependency checks honestly."""
    result = ReadinessService(request.app.state.settings).check()
    return HealthResponse(
        status="ready" if result.ready else "not_ready",
        timestamp_utc=datetime.now(UTC),
        checks=result.checks,
        deferred_checks=list(result.deferred_checks),
    )
