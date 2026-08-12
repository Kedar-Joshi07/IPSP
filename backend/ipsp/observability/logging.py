"""Safe structured runtime logging with local rotating JSONL durability."""

from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from types import TracebackType
from typing import Any
from uuid import uuid4

from ipsp.observability.context import get_request_id, get_trace_id
from ipsp.observability.events import EventStream, new_event
from ipsp.security.redaction import JsonSafeValue, sanitize_structured_data

RUNTIME_LOG_NAME = "ipsp-runtime.jsonl"
DEFAULT_MAX_BYTES = 10 * 1024 * 1024
DEFAULT_BACKUP_COUNT = 5
MAX_EXCEPTION_FRAMES = 32

_OPTIONAL_CONTEXT_FIELDS = (
    "session_correlation_id",
    "user_id",
    "resolved_role",
    "duration_ms",
    "error_code",
    "resource_type",
    "resource_id",
    "project_id",
    "dataset_id",
    "dataset_version_id",
    "semantic_version_id",
    "capability_version_id",
    "model_id",
    "model_version_id",
    "run_id",
    "llm_provider",
    "llm_model",
    "llm_request_id",
)


def sanitize_metadata(value: object) -> JsonSafeValue:
    """Sanitize structured metadata; messages remain developer-controlled constants."""
    return sanitize_structured_data(value)


def _safe_exception_frames(traceback: TracebackType | None) -> list[dict[str, str | int]]:
    frames: list[dict[str, str | int]] = []
    current = traceback
    while current is not None:
        code = current.tb_frame.f_code
        frames.append(
            {
                "file_name": os.path.basename(code.co_filename),
                "function": code.co_name,
                "line_number": current.tb_lineno,
            }
        )
        current = current.tb_next
    return frames[-MAX_EXCEPTION_FRAMES:]


class JsonFormatter(logging.Formatter):
    """Render the canonical safe structured event envelope as one JSON line."""

    def format(self, record: logging.LogRecord) -> str:
        event_id = getattr(record, "ipsp_event_id", None)
        if not event_id:
            event_id = str(uuid4())
            record.ipsp_event_id = event_id
        timestamp_utc = getattr(record, "ipsp_timestamp_utc", None)
        if not isinstance(timestamp_utc, datetime):
            timestamp_utc = datetime.now(UTC)
            record.ipsp_timestamp_utc = timestamp_utc
        trace_id = getattr(record, "ipsp_trace_id", None) or get_trace_id() or str(uuid4())
        request_id = getattr(record, "ipsp_request_id", None) or get_request_id() or str(uuid4())
        record.ipsp_trace_id = trace_id
        record.ipsp_request_id = request_id
        context = {
            field: getattr(record, f"ipsp_{field}", None) for field in _OPTIONAL_CONTEXT_FIELDS
        }
        event = new_event(
            stream=getattr(record, "ipsp_stream", EventStream.APPLICATION),
            component=getattr(record, "ipsp_component", record.name),
            action=getattr(record, "ipsp_action", "log"),
            status=getattr(record, "ipsp_status", record.levelname.lower()),
            severity=record.levelname,
            metadata=getattr(record, "ipsp_metadata", {}),
            timestamp_utc=timestamp_utc,
            event_id=event_id,
            trace_id=trace_id,
            request_id=request_id,
            **context,
        )
        payload: dict[str, Any] = event.as_json_dict()
        payload["message"] = record.getMessage()
        if record.exc_info is not None:
            exception_type, _, traceback = record.exc_info
            if exception_type is not None:
                payload["exception_type"] = exception_type.__name__
            payload["exception_frames"] = _safe_exception_frames(traceback)
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def _owned_handler(handler: logging.Handler) -> bool:
    return bool(getattr(handler, "ipsp_handler", False))


def configure_logging(
    level: str,
    log_dir: Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT,
) -> None:
    """Replace only IPSP-owned handlers with console and rotating local JSONL sinks."""
    log_dir.mkdir(parents=True, exist_ok=True)
    app_logger = logging.getLogger("ipsp")
    app_logger.setLevel(level)
    app_logger.disabled = False
    app_logger.propagate = False
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("ipsp."):
            logging.getLogger(logger_name).disabled = False

    for old_handler in [handler for handler in app_logger.handlers if _owned_handler(handler)]:
        app_logger.removeHandler(old_handler)
        old_handler.close()

    formatter = JsonFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.ipsp_handler = True  # type: ignore[attr-defined]
    stream_handler.ipsp_sink = "console"  # type: ignore[attr-defined]

    file_handler = RotatingFileHandler(
        log_dir / RUNTIME_LOG_NAME,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.ipsp_handler = True  # type: ignore[attr-defined]
    file_handler.ipsp_sink = "runtime_jsonl"  # type: ignore[attr-defined]

    app_logger.addHandler(stream_handler)
    app_logger.addHandler(file_handler)
