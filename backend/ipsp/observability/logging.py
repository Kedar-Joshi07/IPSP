"""Safe JSON logging built on the Python standard library."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from ipsp.observability.context import get_request_id, get_trace_id
from ipsp.security.redaction import JsonSafeValue, sanitize_structured_data

_OPTIONAL_CONTEXT_FIELDS = {
    "ipsp_session_correlation_id": "session_correlation_id",
    "ipsp_user_id": "user_id",
    "ipsp_resolved_role": "resolved_role",
    "ipsp_duration_ms": "duration_ms",
    "ipsp_error_code": "error_code",
    "ipsp_resource_type": "resource_type",
    "ipsp_resource_id": "resource_id",
    "ipsp_project_id": "project_id",
    "ipsp_dataset_id": "dataset_id",
    "ipsp_dataset_version_id": "dataset_version_id",
    "ipsp_semantic_version_id": "semantic_version_id",
    "ipsp_capability_version_id": "capability_version_id",
    "ipsp_model_id": "model_id",
    "ipsp_model_version_id": "model_version_id",
    "ipsp_run_id": "run_id",
    "ipsp_llm_provider": "llm_provider",
    "ipsp_llm_model": "llm_model",
    "ipsp_llm_request_id": "llm_request_id",
}


def sanitize_metadata(value: object) -> JsonSafeValue:
    """Sanitize structured metadata; callers must never put secrets in log messages."""
    return sanitize_structured_data(value)


class JsonFormatter(logging.Formatter):
    """Render the minimum safe structured event envelope as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "event_id": str(uuid4()),
            "trace_id": getattr(record, "ipsp_trace_id", None) or get_trace_id(),
            "request_id": getattr(record, "ipsp_request_id", None) or get_request_id(),
            "component": getattr(record, "ipsp_component", record.name),
            "action": getattr(record, "ipsp_action", "log"),
            "status": getattr(record, "ipsp_status", record.levelname.lower()),
            "severity": record.levelname,
            # Free-form messages cannot be reliably sanitized.
            # Callers must never interpolate secrets into them.
            "message": record.getMessage(),
            "metadata": sanitize_metadata(getattr(record, "ipsp_metadata", {})),
        }
        for record_field, envelope_field in _OPTIONAL_CONTEXT_FIELDS.items():
            value = getattr(record, record_field, None)
            if value is not None:
                payload[envelope_field] = sanitize_structured_data(value)
        if record.exc_info is not None:
            exception_type = record.exc_info[0]
            if exception_type is not None:
                payload["exception_type"] = exception_type.__name__
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def configure_logging(level: str) -> None:
    """Configure the IPSP logger once without altering unrelated root handlers."""
    app_logger = logging.getLogger("ipsp")
    app_logger.setLevel(level)
    app_logger.propagate = False
    if not any(getattr(handler, "ipsp_handler", False) for handler in app_logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        handler.ipsp_handler = True  # type: ignore[attr-defined]
        app_logger.addHandler(handler)
