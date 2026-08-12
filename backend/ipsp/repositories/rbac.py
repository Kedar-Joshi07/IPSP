"""Concrete synchronous repositories for role-to-permission authority."""

from collections.abc import Iterable

from sqlalchemy import delete, exists, select
from sqlalchemy.orm import Session

from ipsp.database.models import Permission, Role, RolePermission, User


class PermissionRepository:
    """Permission catalog persistence without transaction ownership."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_code(self, code: str) -> Permission | None:
        return self._session.scalar(select(Permission).where(Permission.code == code))

    def get_by_codes(self, codes: set[str]) -> dict[str, Permission]:
        if not codes:
            return {}
        permissions = self._session.scalars(
            select(Permission).where(Permission.code.in_(codes))
        ).all()
        return {permission.code: permission for permission in permissions}

    def add(self, permission: Permission) -> None:
        self._session.add(permission)


class RBACRepository:
    """Current role-mapping authority queries and mutations."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def user_has_permission(self, user_id: int, permission_code: str) -> bool:
        statement = select(
            exists().where(
                User.id == user_id,
                User.is_active.is_(True),
                Role.id == User.role_id,
                RolePermission.role_id == Role.id,
                Permission.id == RolePermission.permission_id,
                Permission.code == permission_code,
            )
        )
        return bool(self._session.scalar(statement))

    def list_role_permission_codes(self, role_id: int) -> set[str]:
        return set(
            self._session.scalars(
                select(Permission.code)
                .join(RolePermission, RolePermission.permission_id == Permission.id)
                .where(RolePermission.role_id == role_id)
            )
        )

    def add_role_permissions(self, role_id: int, permission_ids: Iterable[int]) -> None:
        self._session.add_all(
            RolePermission(role_id=role_id, permission_id=permission_id)
            for permission_id in permission_ids
        )

    def replace_role_permissions(self, role_id: int, permission_ids: Iterable[int]) -> None:
        self._session.execute(delete(RolePermission).where(RolePermission.role_id == role_id))
        self.add_role_permissions(role_id, permission_ids)

    def delete_role_permissions_by_codes(self, role_id: int, permission_codes: set[str]) -> None:
        if not permission_codes:
            return
        permission_ids = select(Permission.id).where(Permission.code.in_(permission_codes))
        self._session.execute(
            delete(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id.in_(permission_ids),
            )
        )
