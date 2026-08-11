"""Request and trace context propagation without session data."""

from __future__ import annotations

import logging
import re
import time
from contextvars import ContextVar
from typing import Final
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

_request_id: ContextVar[str] = ContextVar("request_id", default="")
_trace_id: ContextVar[str] = ContextVar("trace_id", default="")
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


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach safe request/trace identifiers and make them available to logs."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = _safe_correlation_id(request.headers.get("X-Request-ID"))
        trace_id = _safe_correlation_id(request.headers.get("X-Trace-ID"))
        request.state.request_id = request_id
        request.state.trace_id = trace_id
        request_token = _request_id.set(request_id)
        trace_token = _trace_id.set(trace_id)
        started = time.perf_counter()

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Trace-ID"] = trace_id
            logger.info(
                "Request completed",
                extra={
                    "ipsp_action": "http.request",
                    "ipsp_status": "success" if response.status_code < 400 else "failure",
                    "ipsp_duration_ms": round((time.perf_counter() - started) * 1000, 3),
                    "ipsp_metadata": {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                    },
                },
            )
            return response
        finally:
            _request_id.reset(request_token)
            _trace_id.reset(trace_token)
