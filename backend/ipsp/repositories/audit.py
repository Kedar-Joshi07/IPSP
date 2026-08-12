"""Append-only synchronous persistence for durable audit events."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ipsp.database.models import AuditEvent


class AuditEventRepository:
    """Audit reads and inserts without commit, update, or delete ownership."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, event: AuditEvent) -> None:
        self._session.add(event)

    def get_by_event_id(self, event_id: str) -> AuditEvent | None:
        return self._session.scalar(select(AuditEvent).where(AuditEvent.event_id == event_id))

    def list_recent(self, limit: int = 100) -> list[AuditEvent]:
        return list(
            self._session.scalars(
                select(AuditEvent).order_by(AuditEvent.timestamp_utc.desc()).limit(limit)
            )
        )

    def count(self) -> int:
        return int(self._session.scalar(select(func.count()).select_from(AuditEvent)) or 0)
