"""Authentication and CSRF dependencies without permission enforcement."""

from typing import Annotated, cast

from fastapi import Depends, Request

from ipsp.auth.service import AuthPrincipal, AuthService
from ipsp.observability.context import bind_authenticated_context


def get_auth_service(request: Request) -> AuthService:
    return cast(AuthService, request.app.state.foundation_services.auth_service)


def _authenticate_session(
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthPrincipal:
    """Perform synchronous session/database work in FastAPI's worker thread."""
    settings = request.app.state.settings.auth
    return auth_service.authenticate_session(request.cookies.get(settings.session_cookie_name))


async def require_authenticated_session(
    request: Request,
    principal: Annotated[AuthPrincipal, Depends(_authenticate_session)],
) -> AuthPrincipal:
    """Bind authenticated identity in the request task after synchronous authentication."""
    request.state.user_id = principal.user_id
    request.state.session_correlation_id = principal.session_correlation_id
    request.state.role_id = principal.role_id
    request.state.role_name = principal.role_name
    bind_authenticated_context(
        session_correlation_id=principal.session_correlation_id,
        user_id=principal.user_id,
        resolved_role=principal.role_name,
    )
    return principal


def require_csrf(
    request: Request,
    principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthPrincipal:
    settings = request.app.state.settings.auth
    auth_service.validate_csrf(
        principal,
        request.cookies.get(settings.csrf_cookie_name),
        request.headers.get(settings.csrf_header_name),
    )
    return principal
