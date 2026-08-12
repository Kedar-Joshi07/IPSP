"""Reusable server-side permission enforcement dependencies."""

from __future__ import annotations

from collections.abc import Callable
from typing import Annotated, cast

from fastapi import Depends, Request

from ipsp.api.dependencies.auth import require_authenticated_session
from ipsp.auth.rbac import CorePermission, RBACService
from ipsp.auth.service import AuthPrincipal


def get_rbac_service(request: Request) -> RBACService:
    return cast(RBACService, request.app.state.foundation_services.rbac_service)


def require_permission(
    permission_code: str | CorePermission,
) -> Callable[..., AuthPrincipal]:
    """Build a dependency that authenticates then checks current database authority."""

    def enforce(
        principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
        rbac_service: Annotated[RBACService, Depends(get_rbac_service)],
    ) -> AuthPrincipal:
        rbac_service.enforce_permission(principal.user_id, permission_code)
        return principal

    return enforce
