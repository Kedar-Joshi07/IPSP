"""Canonical structured event envelope shared by runtime and durable observability."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from ipsp.observability.context import current_observability_context
from ipsp.security.redaction import JsonSafeValue, sanitize_structured_data


class EventStream(StrEnum):
    """Frozen logical observability streams."""

    AUDIT = "audit"
    SECURITY = "security"
    APPLICATION = "application"
    FRONTEND = "frontend"
    DATA_PROCESSING = "data_processing"
    ML = "ml"
    LLM = "llm"
    SIMULATION = "simulation"
    PERFORMANCE = "performance"
    EXPORT = "export"
    ERRORS = "errors"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Sanitized immutable event data suitable for JSON or audit persistence."""

    timestamp_utc: datetime
    event_id: str
    stream: EventStream
    trace_id: str
    request_id: str
    component: str
    action: str
    status: str
    severity: str
    metadata: JsonSafeValue = field(default_factory=dict)
    session_correlation_id: str | None = None
    user_id: int | None = None
    resolved_role: str | None = None
    duration_ms: float | None = None
    error_code: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    project_id: str | None = None
    dataset_id: str | None = None
    dataset_version_id: str | None = None
    semantic_version_id: str | None = None
    capability_version_id: str | None = None
    model_id: str | None = None
    model_version_id: str | None = None
    run_id: str | None = None
    llm_provider: str | None = None
    llm_model: str | None = None
    llm_request_id: str | None = None

    def as_json_dict(self) -> dict[str, Any]:
        """Return an ISO-timestamp mapping while omitting absent optional context."""
        payload = asdict(self)
        payload["timestamp_utc"] = self.timestamp_utc.isoformat()
        payload["stream"] = self.stream.value
        return {key: value for key, value in payload.items() if value is not None}


def new_event(
    *,
    stream: EventStream | str,
    component: str,
    action: str,
    status: str,
    severity: str,
    metadata: object | None = None,
    timestamp_utc: datetime | None = None,
    event_id: str | None = None,
    trace_id: str | None = None,
    request_id: str | None = None,
    **context_overrides: object,
) -> EventEnvelope:
    """Create a canonical event with generated correlation when no HTTP context exists."""
    context = current_observability_context()
    effective_trace_id = trace_id or context.trace_id or str(uuid4())
    effective_request_id = request_id or context.request_id or str(uuid4())
    optional: dict[str, object] = {
        "session_correlation_id": context.session_correlation_id,
        "user_id": context.user_id,
        "resolved_role": context.resolved_role,
        "resource_type": context.resource_type,
        "resource_id": context.resource_id,
    }
    optional.update({key: value for key, value in context_overrides.items() if value is not None})
    return EventEnvelope(
        timestamp_utc=timestamp_utc or datetime.now(UTC),
        event_id=event_id or str(uuid4()),
        stream=EventStream(stream),
        trace_id=effective_trace_id,
        request_id=effective_request_id,
        component=component,
        action=action,
        status=status,
        severity=severity.upper(),
        metadata=sanitize_structured_data(metadata or {}),
        session_correlation_id=_optional_str(optional.get("session_correlation_id")),
        user_id=_optional_int(optional.get("user_id")),
        resolved_role=_optional_str(optional.get("resolved_role")),
        duration_ms=_optional_float(optional.get("duration_ms")),
        error_code=_optional_str(optional.get("error_code")),
        resource_type=_optional_str(optional.get("resource_type")),
        resource_id=_optional_str(optional.get("resource_id")),
        project_id=_optional_str(optional.get("project_id")),
        dataset_id=_optional_str(optional.get("dataset_id")),
        dataset_version_id=_optional_str(optional.get("dataset_version_id")),
        semantic_version_id=_optional_str(optional.get("semantic_version_id")),
        capability_version_id=_optional_str(optional.get("capability_version_id")),
        model_id=_optional_str(optional.get("model_id")),
        model_version_id=_optional_str(optional.get("model_version_id")),
        run_id=_optional_str(optional.get("run_id")),
        llm_provider=_optional_str(optional.get("llm_provider")),
        llm_model=_optional_str(optional.get("llm_model")),
        llm_request_id=_optional_str(optional.get("llm_request_id")),
    )


def _optional_str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _optional_int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _optional_float(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    return None
