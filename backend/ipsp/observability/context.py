"""Isolated request, trace, and authenticated observability context."""

from __future__ import annotations

import logging
import re
import time
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Final
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

_request_id: ContextVar[str] = ContextVar("request_id", default="")
_trace_id: ContextVar[str] = ContextVar("trace_id", default="")
_session_correlation_id: ContextVar[str | None] = ContextVar("session_correlation_id", default=None)
_user_id: ContextVar[int | None] = ContextVar("user_id", default=None)
_resolved_role: ContextVar[str | None] = ContextVar("resolved_role", default=None)
_SAFE_CORRELATION_ID: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")

logger = logging.getLogger("ipsp.request")


def _safe_correlation_id(value: str | None) -> str:
    if value is not None and _SAFE_CORRELATION_ID.fullmatch(value):
        return value
    return str(uuid4())


def get_request_id() -> str:
    """Return the active request identifier, if any."""
    return _request_id.get()


def get_trace_id() -> str:
    """Return the active trace identifier, if any."""
    return _trace_id.get()


@dataclass(frozen=True, slots=True)
class ObservabilityContext:
    """Current non-secret correlation and authenticated identity values."""

    request_id: str
    trace_id: str
    session_correlation_id: str | None
    user_id: int | None
    resolved_role: str | None


def current_observability_context() -> ObservabilityContext:
    """Read the active context without exposing browser bearer credentials."""
    return ObservabilityContext(
        request_id=_request_id.get(),
        trace_id=_trace_id.get(),
        session_correlation_id=_session_correlation_id.get(),
        user_id=_user_id.get(),
        resolved_role=_resolved_role.get(),
    )


def bind_authenticated_context(
    *, session_correlation_id: str, user_id: int, resolved_role: str
) -> None:
    """Bind safe identity only after successful server-session authentication."""
    _session_correlation_id.set(session_correlation_id)
    _user_id.set(user_id)
    _resolved_role.set(resolved_role)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach safe request/trace identifiers and make them available to logs."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = _safe_correlation_id(request.headers.get("X-Request-ID"))
        trace_id = _safe_correlation_id(request.headers.get("X-Trace-ID"))
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        request_token = _request_id.set(request_id)
        trace_token = _trace_id.set(trace_id)
        session_token = _session_correlation_id.set(None)
        user_token = _user_id.set(None)
        role_token = _resolved_role.set(None)
        started = time.perf_counter()

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Trace-ID"] = trace_id
            logger.info(
                "Request completed",
                extra={
                    "ipsp_action": "http.request",
                    "ipsp_stream": "performance",
                    "ipsp_component": "api",
                    "ipsp_status": "success" if response.status_code < 400 else "failure",
                    "ipsp_duration_ms": round((time.perf_counter() - started) * 1000, 3),
                    "ipsp_session_correlation_id": getattr(
                        request.state, "session_correlation_id", None
                    ),
                    "ipsp_user_id": getattr(request.state, "user_id", None),
                    "ipsp_resolved_role": getattr(request.state, "role_name", None),
                    "ipsp_metadata": {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                    },
                },
            )
            return response
        finally:
            _resolved_role.reset(role_token)
            _user_id.reset(user_token)
            _session_correlation_id.reset(session_token)
            _request_id.reset(request_token)
            _trace_id.reset(trace_token)
