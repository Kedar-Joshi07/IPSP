"""Authorized versioned system diagnostic routes."""

from typing import Annotated, cast

from fastapi import APIRouter, Depends, Request

from ipsp.api.dependencies.rbac import require_permission
from ipsp.api.schemas.system_health import SystemHealthResponse
from ipsp.auth.rbac import CorePermission
from ipsp.auth.service import AuthPrincipal
from ipsp.services.system_health import SystemHealthService

router = APIRouter(prefix="/admin/system", tags=["admin-system"])
_require_system_configure = require_permission(CorePermission.SYSTEM_CONFIGURE)


def get_system_health_service(request: Request) -> SystemHealthService:
    return cast(SystemHealthService, request.app.state.foundation_services.system_health_service)


@router.get("/health", response_model=SystemHealthResponse)
def system_health(
    _principal: Annotated[AuthPrincipal, Depends(_require_system_configure)],
    service: Annotated[SystemHealthService, Depends(get_system_health_service)],
) -> SystemHealthResponse:
    """Return sanitized rich diagnostics to current permission holders."""
    return SystemHealthResponse.model_validate(service.check())
