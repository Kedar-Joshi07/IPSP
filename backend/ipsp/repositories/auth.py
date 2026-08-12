"""Concrete repositories for authentication identity and sessions."""

from datetime import datetime

from sqlalchemy import Select, func, select, update
from sqlalchemy.orm import Session

from ipsp.database.models import Role, User, UserSession


class UserRepository:
    """Synchronous user persistence without transaction ownership."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, user_id: int) -> User | None:
        return self._session.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self._session.scalar(select(User).where(User.username == username))

    def count(self) -> int:
        return int(self._session.scalar(select(func.count()).select_from(User)) or 0)

    def add(self, user: User) -> None:
        self._session.add(user)

    def list_ids_by_role(self, role_id: int) -> list[int]:
        return list(self._session.scalars(select(User.id).where(User.role_id == role_id)))

    @staticmethod
    def record_failed_login(user: User, timestamp: datetime, locked_until: datetime | None) -> None:
        user.failed_login_count += 1
        user.locked_until = locked_until
        user.updated_at = timestamp

    @staticmethod
    def record_successful_login(
        user: User, timestamp: datetime, replacement_hash: str | None
    ) -> None:
        user.failed_login_count = 0
        user.locked_until = None
        user.last_login_at = timestamp
        user.updated_at = timestamp
        if replacement_hash is not None:
            user.password_hash = replacement_hash

    @staticmethod
    def replace_password(user: User, password_hash: str, timestamp: datetime) -> None:
        user.password_hash = password_hash
        user.password_changed_at = timestamp
        user.must_change_password = False
        user.failed_login_count = 0
        user.locked_until = None
        user.updated_at = timestamp


class RoleRepository:
    """Synchronous role lookup and bootstrap persistence."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, role_id: int) -> Role | None:
        return self._session.get(Role, role_id)

    def get_by_name(self, name: str) -> Role | None:
        return self._session.scalar(select(Role).where(Role.name == name))

    def add(self, role: Role) -> None:
        self._session.add(role)


class UserSessionRepository:
    """Synchronous hash-indexed server-session persistence."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, user_session: UserSession) -> None:
        self._session.add(user_session)

    def get_by_id(self, session_id: int) -> UserSession | None:
        return self._session.get(UserSession, session_id)

    def get_by_token_hash(self, token_hash: str) -> UserSession | None:
        statement: Select[tuple[UserSession]] = select(UserSession).where(
            UserSession.token_hash == token_hash
        )
        return self._session.scalar(statement)

    @staticmethod
    def update_last_seen(user_session: UserSession, timestamp: datetime) -> None:
        user_session.last_seen_at = timestamp

    def invalidate_one(self, session_id: int, timestamp: datetime) -> None:
        self._session.execute(
            update(UserSession)
            .where(UserSession.id == session_id, UserSession.invalidated_at.is_(None))
            .values(invalidated_at=timestamp)
        )

    def invalidate_by_token_hash(self, token_hash: str, timestamp: datetime) -> None:
        self._session.execute(
            update(UserSession)
            .where(UserSession.token_hash == token_hash, UserSession.invalidated_at.is_(None))
            .values(invalidated_at=timestamp)
        )

    def invalidate_all_by_user(self, user_id: int, timestamp: datetime) -> None:
        self._session.execute(
            update(UserSession)
            .where(UserSession.user_id == user_id, UserSession.invalidated_at.is_(None))
            .values(invalidated_at=timestamp)
        )
