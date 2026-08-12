"""Central browser cookie policy for opaque authentication sessions."""

from fastapi import Response

from ipsp.auth.service import LoginResult
from ipsp.config.settings import AuthSettings


def set_auth_cookies(response: Response, settings: AuthSettings, result: LoginResult) -> None:
    """Set session and CSRF cookies with one aligned lifetime and policy."""
    max_age = settings.session_ttl_minutes * 60
    response.set_cookie(
        settings.session_cookie_name,
        result.session_token,
        max_age=max_age,
        expires=result.principal.session_expires_at,
        path="/",
        secure=settings.cookie_secure,
        httponly=True,
        samesite=settings.cookie_samesite,
    )
    response.set_cookie(
        settings.csrf_cookie_name,
        result.csrf_token,
        max_age=max_age,
        expires=result.principal.session_expires_at,
        path="/",
        secure=settings.cookie_secure,
        httponly=False,
        samesite=settings.cookie_samesite,
    )


def clear_auth_cookies(response: Response, settings: AuthSettings) -> None:
    """Expire both authentication cookies using their original scope and flags."""
    response.delete_cookie(
        settings.session_cookie_name,
        path="/",
        secure=settings.cookie_secure,
        httponly=True,
        samesite=settings.cookie_samesite,
    )
    response.delete_cookie(
        settings.csrf_cookie_name,
        path="/",
        secure=settings.cookie_secure,
        httponly=False,
        samesite=settings.cookie_samesite,
    )
