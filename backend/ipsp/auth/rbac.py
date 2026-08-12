"""Current-database RBAC enforcement and additive core provisioning."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy.orm import Session

from ipsp.database.models import Permission, Role
from ipsp.database.session import DatabaseSessionFactory
from ipsp.errors.exceptions import IPSPError, PermissionDeniedException
from ipsp.observability.audit import AuditService
from ipsp.observability.events import EventStream
from ipsp.repositories.auth import RoleRepository, UserRepository, UserSessionRepository
from ipsp.repositories.rbac import PermissionRepository, RBACRepository


class CorePermission(StrEnum):
    """Typed first-party permission codes; persisted permission data remains extensible."""

    SIMULATION_RUN = "simulation.run"
    SIMULATION_EXPORT = "simulation.export"
    DATASET_VIEW = "dataset.view"
    DATASET_UPLOAD = "dataset.upload"
    DATASET_CONFIGURE = "dataset.configure"
    DATASET_ASSIGN = "dataset.assign"
    MODEL_TRAIN = "model.train"
    MODEL_PROMOTE = "model.promote"
    LLM_CONFIGURE = "llm.configure"
    INTERNET_CONFIGURE = "internet.configure"
    USER_MANAGE = "user.manage"
    LOGS_VIEW = "logs.view"
    SYSTEM_CONFIGURE = "system.configure"


CORE_PERMISSION_CODES = frozenset(permission.value for permission in CorePermission)


def _now() -> datetime:
    return datetime.now(UTC)


def _invalid_change() -> IPSPError:
    return IPSPError("AUTHZ-RBAC_INVALID", "Authorization change could not be applied.")


@dataclass(frozen=True, slots=True)
class CatalogSyncResult:
    """Non-secret counts describing one additive catalog synchronization."""

    roles_created: int
    permissions_created: int
    admin_mappings_created: int
    sessions_invalidated_for_users: int

    @property
    def changed(self) -> bool:
        return bool(self.roles_created or self.permissions_created or self.admin_mappings_created)


class RBACService:
    """Resolve current persisted authority and apply narrow privilege mutations."""

    def __init__(self, sessions: DatabaseSessionFactory, audit: AuditService) -> None:
        self._sessions = sessions
        self._audit = audit

    def has_permission(self, user_id: int, permission_code: str | CorePermission) -> bool:
        code = str(permission_code)
        if not code or "*" in code:
            return False
        with self._sessions.session() as session:
            return RBACRepository(session).user_has_permission(user_id, code)

    def enforce_permission(
        self,
        user_id: int,
        permission_code: str | CorePermission,
        *,
        session_correlation_id: str | None = None,
        resolved_role: str | None = None,
    ) -> None:
        if not self.has_permission(user_id, permission_code):
            self._audit.record(
                stream=EventStream.SECURITY,
                component="rbac",
                action="rbac.permission_denied",
                status="failure",
                severity="WARNING",
                error_code="AUTHZ-PERMISSION_DENIED",
                user_id=user_id,
                resolved_role=resolved_role,
                session_correlation_id=session_correlation_id,
                metadata={"permission_code": str(permission_code)},
            )
            raise PermissionDeniedException()

    def assign_user_role(
        self,
        user_id: int,
        role_id: int,
        timestamp: datetime | None = None,
    ) -> bool:
        now = timestamp or _now()
        with self._sessions.transaction() as session:
            users = UserRepository(session)
            user = users.get_by_id(user_id)
            role = RoleRepository(session).get_by_id(role_id)
            if user is None or role is None:
                raise _invalid_change()
            if user.role_id == role_id:
                return False
            user.role_id = role_id
            user.updated_at = now
            UserSessionRepository(session).invalidate_all_by_user(user_id, now)
            self._audit.record_in_session(
                session,
                stream=EventStream.AUDIT,
                component="rbac",
                action="rbac.user_role_change",
                status="success",
                severity="INFO",
                user_id=user_id,
                resource_type="role",
                resource_id=str(role_id),
            )
        return True

    def replace_role_permissions(
        self,
        role_id: int,
        permission_codes: set[str | CorePermission],
        timestamp: datetime | None = None,
    ) -> bool:
        now = timestamp or _now()
        requested = {str(code) for code in permission_codes}
        if any(not code or "*" in code for code in requested):
            raise _invalid_change()
        with self._sessions.transaction() as session:
            if RoleRepository(session).get_by_id(role_id) is None:
                raise _invalid_change()
            permission_repository = PermissionRepository(session)
            permissions = permission_repository.get_by_codes(requested)
            if set(permissions) != requested:
                raise _invalid_change()
            rbac = RBACRepository(session)
            existing = rbac.list_role_permission_codes(role_id)
            if existing == requested:
                return False
            rbac.delete_role_permissions_by_codes(role_id, existing - requested)
            rbac.add_role_permissions(
                role_id,
                (permissions[code].id for code in sorted(requested - existing)),
            )
            user_ids = UserRepository(session).list_ids_by_role(role_id)
            user_sessions = UserSessionRepository(session)
            for user_id in user_ids:
                user_sessions.invalidate_all_by_user(user_id, now)
            self._audit.record_in_session(
                session,
                stream=EventStream.AUDIT,
                component="rbac",
                action="rbac.role_permissions_change",
                status="success",
                severity="INFO",
                resource_type="role",
                resource_id=str(role_id),
                metadata={"permission_codes": sorted(requested)},
            )
        return True


class RBACCatalogService:
    """Additively provision core roles, permissions, and explicit Admin mappings."""

    def __init__(self, sessions: DatabaseSessionFactory, audit: AuditService) -> None:
        self._sessions = sessions
        self._audit = audit

    def ensure_core_catalog(self, timestamp: datetime | None = None) -> CatalogSyncResult:
        with self._sessions.transaction() as session:
            result = self.ensure_core_catalog_in_session(session, timestamp or _now(), self._audit)
            return result

    @staticmethod
    def ensure_core_catalog_in_session(
        session: Session,
        timestamp: datetime,
        audit: AuditService | None = None,
    ) -> CatalogSyncResult:
        result = RBACCatalogService._apply_core_catalog(session, timestamp)
        if result.changed and audit is not None:
            audit.record_in_session(
                session,
                stream=EventStream.AUDIT,
                component="rbac",
                action="rbac.catalog_sync",
                status="success",
                severity="INFO",
                metadata={
                    "roles_created": result.roles_created,
                    "permissions_created": result.permissions_created,
                    "admin_mappings_created": result.admin_mappings_created,
                    "session_users_invalidated": result.sessions_invalidated_for_users,
                },
            )
        return result

    @staticmethod
    def _apply_core_catalog(session: Session, timestamp: datetime) -> CatalogSyncResult:
        """Apply catalog changes; caller owns transaction and optional audit insertion."""
        roles = RoleRepository(session)
        permissions = PermissionRepository(session)
        rbac = RBACRepository(session)
        roles_created = 0
        permissions_created = 0

        admin_role = roles.get_by_name("Admin")
        if admin_role is None:
            admin_role = Role(name="Admin", description="Platform administration role")
            roles.add(admin_role)
            roles_created += 1
        if roles.get_by_name("User") is None:
            roles.add(Role(name="User", description="Standard platform user role"))
            roles_created += 1

        core_permissions = permissions.get_by_codes(set(CORE_PERMISSION_CODES))
        for code in sorted(CORE_PERMISSION_CODES - set(core_permissions)):
            permission = Permission(code=code, description=None)
            permissions.add(permission)
            core_permissions[code] = permission
            permissions_created += 1
        session.flush()

        existing_admin_codes = rbac.list_role_permission_codes(admin_role.id)
        missing_admin_codes = CORE_PERMISSION_CODES - existing_admin_codes
        rbac.add_role_permissions(
            admin_role.id,
            (core_permissions[code].id for code in sorted(missing_admin_codes)),
        )

        affected_user_ids = (
            UserRepository(session).list_ids_by_role(admin_role.id) if missing_admin_codes else []
        )
        user_sessions = UserSessionRepository(session)
        for user_id in affected_user_ids:
            user_sessions.invalidate_all_by_user(user_id, timestamp)

        return CatalogSyncResult(
            roles_created=roles_created,
            permissions_created=permissions_created,
            admin_mappings_created=len(missing_admin_codes),
            sessions_invalidated_for_users=len(affected_user_ids),
        )
