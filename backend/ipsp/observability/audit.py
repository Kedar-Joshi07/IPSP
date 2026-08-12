"""Durable selected audit/security event orchestration."""

from __future__ import annotations

import json

from sqlalchemy.orm import Session

from ipsp.database.models import AuditEvent
from ipsp.database.session import DatabaseSessionFactory
from ipsp.observability.events import EventEnvelope, EventStream, new_event
from ipsp.repositories.audit import AuditEventRepository
from ipsp.security.redaction import JsonSafeValue, sanitize_structured_data


def encode_metadata(metadata: object) -> str:
    """Sanitize and encode metadata deterministically without Python repr."""
    return json.dumps(
        sanitize_structured_data(metadata),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def decode_metadata(metadata_json: str) -> JsonSafeValue:
    """Decode persisted metadata for trusted internal reads and tests."""
    return sanitize_structured_data(json.loads(metadata_json))


class AuditService:
    """Construct and append selected durable events with explicit transactions."""

    def __init__(self, sessions: DatabaseSessionFactory) -> None:
        self._sessions = sessions

    def record(self, **event_fields: object) -> EventEnvelope:
        """Append an event in its own transaction."""
        with self._sessions.transaction() as session:
            return self.record_in_session(session, **event_fields)

    def record_in_session(self, session: Session, **event_fields: object) -> EventEnvelope:
        """Append an event inside the caller's transaction for atomic mutation auditing."""
        event = new_event(**event_fields)  # type: ignore[arg-type]
        if event.stream not in {EventStream.AUDIT, EventStream.SECURITY}:
            raise ValueError("Only audit and security streams may be durably persisted")
        AuditEventRepository(session).add(self._to_model(event))
        return event

    @staticmethod
    def _to_model(event: EventEnvelope) -> AuditEvent:
        return AuditEvent(
            event_id=event.event_id,
            timestamp_utc=event.timestamp_utc,
            stream=event.stream.value,
            trace_id=event.trace_id,
            request_id=event.request_id,
            session_correlation_id=event.session_correlation_id,
            user_id=event.user_id,
            resolved_role=event.resolved_role,
            component=event.component,
            action=event.action,
            status=event.status,
            severity=event.severity,
            duration_ms=event.duration_ms,
            error_code=event.error_code,
            resource_type=event.resource_type,
            resource_id=event.resource_id,
            project_id=event.project_id,
            dataset_id=event.dataset_id,
            dataset_version_id=event.dataset_version_id,
            semantic_version_id=event.semantic_version_id,
            capability_version_id=event.capability_version_id,
            model_id=event.model_id,
            model_version_id=event.model_version_id,
            run_id=event.run_id,
            llm_provider=event.llm_provider,
            llm_model=event.llm_model,
            llm_request_id=event.llm_request_id,
            metadata_json=encode_metadata(event.metadata),
        )
