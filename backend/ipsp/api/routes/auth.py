"""Thin versioned authentication routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status

from ipsp.api.dependencies.auth import (
    get_auth_service,
    require_authenticated_session,
    require_csrf,
)
from ipsp.api.schemas.auth import (
    AuthenticatedIdentityResponse,
    ChangePasswordRequest,
    LoginRequest,
)
from ipsp.auth.cookies import clear_auth_cookies, set_auth_cookies
from ipsp.auth.service import AuthPrincipal, AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


def _identity(principal: AuthPrincipal) -> AuthenticatedIdentityResponse:
    return AuthenticatedIdentityResponse(
        id=principal.user_id,
        username=principal.username,
        display_name=principal.display_name,
        email=principal.email,
        role_id=principal.role_id,
        role_name=principal.role_name,
        must_change_password=principal.must_change_password,
        session_correlation_id=principal.session_correlation_id,
        session_expires_at=principal.session_expires_at,
    )


@router.post("/login", response_model=AuthenticatedIdentityResponse)
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> AuthenticatedIdentityResponse:
    settings = request.app.state.settings.auth
    result = auth_service.login(
        payload.username,
        payload.password.get_secret_value(),
        existing_session_token=request.cookies.get(settings.session_cookie_name),
    )
    set_auth_cookies(response, settings, result)
    response.headers["Cache-Control"] = "no-store"
    return _identity(result.principal)


@router.get("/me", response_model=AuthenticatedIdentityResponse)
def me(
    response: Response,
    principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
) -> AuthenticatedIdentityResponse:
    response.headers["Cache-Control"] = "no-store"
    return _identity(principal)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def logout(
    request: Request,
    principal: Annotated[AuthPrincipal, Depends(require_csrf)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Response:
    auth_service.logout(principal)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    clear_auth_cookies(response, request.app.state.settings.auth)
    response.headers["Cache-Control"] = "no-store"
    return response


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def change_password(
    payload: ChangePasswordRequest,
    request: Request,
    principal: Annotated[AuthPrincipal, Depends(require_csrf)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Response:
    auth_service.change_password(
        principal,
        payload.current_password.get_secret_value(),
        payload.new_password.get_secret_value(),
    )
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    clear_auth_cookies(response, request.app.state.settings.auth)
    response.headers["Cache-Control"] = "no-store"
    return response
