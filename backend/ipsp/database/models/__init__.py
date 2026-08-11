"""Canonical SQLAlchemy ORM metadata ownership location."""

from ipsp.database.models.base import Base, metadata
from ipsp.database.models.security import Permission, Role, RolePermission, User

__all__ = ["Base", "Permission", "Role", "RolePermission", "User", "metadata"]
