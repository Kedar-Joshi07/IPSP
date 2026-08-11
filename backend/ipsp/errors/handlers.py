"""Central FastAPI mappings for domain and unexpected exceptions."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ipsp.api.schemas.common import ErrorResponse
from ipsp.errors.exceptions import IPSPError
from ipsp.security.redaction import sanitize_details

logger = logging.getLogger("ipsp.errors")

_STATUS_BY_PREFIX = {
    "AUTH": 401,
    "AUTHZ": 403,
    "DATA": 422,
    "SEM": 400,
    "REL": 400,
    "ML": 422,
    "LLM": 502,
    "SIM": 422,
    "TRUST": 422,
    "EXP": 500,
    "JOB": 500,
    "SYS": 500,
}


def _trace_id(request: Request) -> str:
    return str(getattr(request.state, "trace_id", "unavailable"))


def _request_id(request: Request) -> str:
    return str(getattr(request.state, "request_id", "unavailable"))


def _response(request: Request, error: ErrorResponse, status_code: int) -> JSONResponse:
    response = JSONResponse(status_code=status_code, content=error.model_dump(mode="json"))
    response.headers["X-Trace-ID"] = error.trace_id
    response.headers["X-Request-ID"] = _request_id(request)
    return response


def register_exception_handlers(app: FastAPI) -> None:
    """Register stable safe error mappings on an application instance."""

    @app.exception_handler(IPSPError)
    async def handle_ipsp_error(request: Request, exc: IPSPError) -> JSONResponse:
        prefix = exc.error_code.partition("-")[0]
        status_code = _STATUS_BY_PREFIX.get(prefix, 500)
        logger.warning(
            "Handled IPSP error",
            extra={
                "ipsp_trace_id": _trace_id(request),
                "ipsp_request_id": _request_id(request),
                "ipsp_action": "exception.handled",
                "ipsp_status": "failure",
                "ipsp_error_code": exc.error_code,
                "ipsp_metadata": {"exception_type": type(exc).__name__},
            },
        )
        return _response(
            request,
            ErrorResponse(
                error_code=exc.error_code,
                message=exc.safe_message,
                trace_id=_trace_id(request),
                recoverable=exc.recoverable,
                details=sanitize_details(exc.details),
            ),
            status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        safe_details: list[dict[str, Any]] = [
            {"location": list(error["loc"]), "message": error["msg"], "type": error["type"]}
            for error in exc.errors()
        ]
        return _response(
            request,
            ErrorResponse(
                error_code="DATA-VALIDATION",
                message="The request could not be validated.",
                trace_id=_trace_id(request),
                details=safe_details,
            ),
            422,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unexpected application error",
            extra={
                "ipsp_trace_id": _trace_id(request),
                "ipsp_request_id": _request_id(request),
                "ipsp_action": "exception.unexpected",
                "ipsp_status": "failure",
                "ipsp_error_code": "SYS-UNEXPECTED",
                "ipsp_metadata": {"exception_type": type(exc).__name__},
            },
        )
        return _response(
            request,
            ErrorResponse(
                error_code="SYS-UNEXPECTED",
                message="An unexpected error occurred. Use the trace ID when requesting support.",
                trace_id=_trace_id(request),
            ),
            500,
        )
