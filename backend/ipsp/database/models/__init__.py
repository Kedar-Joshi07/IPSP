"""Canonical SQLAlchemy ORM metadata ownership location."""

from ipsp.database.models.base import Base, metadata
from ipsp.database.models.jobs import JobRecord
from ipsp.database.models.observability import AuditEvent
from ipsp.database.models.security import Permission, Role, RolePermission, User, UserSession

__all__ = [
    "AuditEvent",
    "Base",
    "JobRecord",
    "Permission",
    "Role",
    "RolePermission",
    "User",
    "UserSession",
    "metadata",
]
