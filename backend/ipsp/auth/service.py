"""Authentication orchestration with explicit transactional ownership."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from ipsp.auth.passwords import PasswordInputError, PasswordService
from ipsp.config.settings import AuthSettings
from ipsp.database.models import Role, User, UserSession
from ipsp.database.session import DatabaseSessionFactory
from ipsp.errors.exceptions import IPSPError
from ipsp.repositories.auth import RoleRepository, UserRepository, UserSessionRepository


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _constant_text_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class AuthPrincipal:
    """Safe authenticated identity and non-secret session context."""

    session_id: int
    user_id: int
    username: str
    display_name: str
    email: str | None
    role_id: int
    role_name: str
    must_change_password: bool
    session_correlation_id: str
    session_expires_at: datetime


@dataclass(frozen=True, slots=True)
class LoginResult:
    """New browser credentials, kept out of repr and JSON response schemas."""

    principal: AuthPrincipal
    session_token: str = field(repr=False)
    csrf_token: str = field(repr=False)


class AuthService:
    """Authenticate identities without applying authorization permissions."""

    def __init__(
        self,
        settings: AuthSettings,
        sessions: DatabaseSessionFactory,
        passwords: PasswordService,
    ) -> None:
        self._settings = settings
        self._sessions = sessions
        self._passwords = passwords

    @staticmethod
    def _invalid_credentials() -> IPSPError:
        return IPSPError("AUTH-INVALID_CREDENTIALS", "Authentication failed.")

    @staticmethod
    def _invalid_session() -> IPSPError:
        return IPSPError("AUTH-SESSION_INVALID", "Authentication session is invalid.")

    @staticmethod
    def _principal(user: User, role: Role, session: UserSession) -> AuthPrincipal:
        assert session.id is not None
        assert user.id is not None
        return AuthPrincipal(
            session_id=session.id,
            user_id=user.id,
            username=user.username,
            display_name=user.display_name,
            email=user.email,
            role_id=role.id,
            role_name=role.name,
            must_change_password=user.must_change_password,
            session_correlation_id=session.session_correlation_id,
            session_expires_at=session.expires_at,
        )

    def login(
        self,
        username: str,
        password: str,
        *,
        existing_session_token: str | None = None,
        timestamp: datetime | None = None,
    ) -> LoginResult:
        now = timestamp or _now()
        if not username or len(username) > 255:
            self._passwords.equalize_unknown_user(password)
            raise self._invalid_credentials()

        failure = False
        result: LoginResult | None = None
        with self._sessions.transaction() as session:
            users = UserRepository(session)
            sessions = UserSessionRepository(session)
            roles = RoleRepository(session)
            user = users.get_by_username(username)
            if (
                user is None
                or not user.is_active
                or (user.locked_until is not None and now < user.locked_until)
            ):
                self._passwords.equalize_unknown_user(password)
                failure = True
            else:
                try:
                    verified, replacement_hash = self._passwords.verify_and_update(
                        password, user.password_hash
                    )
                except (PasswordInputError, ValueError):
                    verified, replacement_hash = False, None
                if not verified:
                    locked_until = None
                    if user.failed_login_count + 1 >= self._settings.failed_login_threshold:
                        locked_until = now + timedelta(minutes=self._settings.lockout_minutes)
                    users.record_failed_login(user, now, locked_until)
                    failure = True
                else:
                    role = roles.get_by_id(user.role_id)
                    if role is None:
                        failure = True
                    else:
                        users.record_successful_login(user, now, replacement_hash)
                        if existing_session_token:
                            sessions.invalidate_by_token_hash(_digest(existing_session_token), now)
                        raw_session = secrets.token_urlsafe(32)
                        raw_csrf = secrets.token_urlsafe(32)
                        user_session = UserSession(
                            token_hash=_digest(raw_session),
                            csrf_token_hash=_digest(raw_csrf),
                            session_correlation_id=str(uuid.uuid4()),
                            user_id=user.id,
                            created_at=now,
                            last_seen_at=now,
                            expires_at=now + timedelta(minutes=self._settings.session_ttl_minutes),
                            invalidated_at=None,
                        )
                        sessions.add(user_session)
                        session.flush()
                        result = LoginResult(
                            principal=self._principal(user, role, user_session),
                            session_token=raw_session,
                            csrf_token=raw_csrf,
                        )
        if failure or result is None:
            raise self._invalid_credentials()
        return result

    def authenticate_session(
        self, token: str | None, *, timestamp: datetime | None = None
    ) -> AuthPrincipal:
        if not token:
            raise IPSPError("AUTH-SESSION_REQUIRED", "Authentication is required.")
        now = timestamp or _now()
        principal: AuthPrincipal | None = None
        with self._sessions.transaction() as session:
            sessions = UserSessionRepository(session)
            users = UserRepository(session)
            roles = RoleRepository(session)
            user_session = sessions.get_by_token_hash(_digest(token))
            if user_session is not None and user_session.invalidated_at is None:
                if now >= user_session.expires_at:
                    sessions.invalidate_one(user_session.id, now)
                else:
                    user = users.get_by_id(user_session.user_id)
                    if user is None or not user.is_active:
                        if user is not None:
                            sessions.invalidate_all_by_user(user.id, now)
                        else:
                            sessions.invalidate_one(user_session.id, now)
                    else:
                        role = roles.get_by_id(user.role_id)
                        if role is not None:
                            sessions.update_last_seen(user_session, now)
                            principal = self._principal(user, role, user_session)
        if principal is None:
            raise self._invalid_session()
        return principal

    def validate_csrf(
        self,
        principal: AuthPrincipal,
        csrf_cookie: str | None,
        csrf_header: str | None,
    ) -> None:
        valid = bool(csrf_cookie and csrf_header and _constant_text_equal(csrf_cookie, csrf_header))
        stored_hash: str | None = None
        with self._sessions.session() as session:
            user_session = UserSessionRepository(session).get_by_id(principal.session_id)
            if user_session is not None:
                stored_hash = user_session.csrf_token_hash
        if (
            not valid
            or stored_hash is None
            or not hmac.compare_digest(_digest(csrf_cookie or ""), stored_hash)
        ):
            raise IPSPError("AUTHZ-CSRF_INVALID", "CSRF validation failed.")

    def logout(self, principal: AuthPrincipal, *, timestamp: datetime | None = None) -> None:
        with self._sessions.transaction() as session:
            UserSessionRepository(session).invalidate_one(principal.session_id, timestamp or _now())

    def change_password(
        self,
        principal: AuthPrincipal,
        current_password: str,
        new_password: str,
        *,
        timestamp: datetime | None = None,
    ) -> None:
        now = timestamp or _now()
        failure = False
        try:
            self._passwords.validate(new_password)
        except PasswordInputError:
            raise IPSPError("AUTH-PASSWORD_INVALID", "New password is invalid.") from None
        with self._sessions.transaction() as session:
            users = UserRepository(session)
            user = users.get_by_id(principal.user_id)
            if user is None:
                failure = True
            else:
                try:
                    verified = self._passwords.verify(current_password, user.password_hash)
                except (PasswordInputError, ValueError):
                    verified = False
                if not verified:
                    failure = True
                else:
                    new_hash = self._passwords.hash(new_password)
                    users.replace_password(user, new_hash, now)
                    UserSessionRepository(session).invalidate_all_by_user(user.id, now)
        if failure:
            raise IPSPError("AUTH-PASSWORD_INVALID", "Current password is invalid.")

    def invalidate_all_user_sessions(self, user_id: int, timestamp: datetime | None = None) -> None:
        with self._sessions.transaction() as session:
            UserSessionRepository(session).invalidate_all_by_user(user_id, timestamp or _now())

    def bootstrap_admin(
        self,
        username: str,
        display_name: str,
        email: str | None,
        password: str,
        *,
        timestamp: datetime | None = None,
    ) -> int:
        if not username or len(username) > 255 or not display_name or len(display_name) > 255:
            raise IPSPError("AUTH-BOOTSTRAP_UNAVAILABLE", "Admin bootstrap input is invalid.")
        now = timestamp or _now()
        user_id: int | None = None
        with self._sessions.transaction() as session:
            users = UserRepository(session)
            roles = RoleRepository(session)
            if users.count() != 0:
                raise IPSPError(
                    "AUTH-BOOTSTRAP_UNAVAILABLE", "Admin bootstrap is no longer available."
                )
            try:
                password_hash = self._passwords.hash(password)
            except PasswordInputError:
                raise IPSPError(
                    "AUTH-BOOTSTRAP_UNAVAILABLE", "Admin bootstrap input is invalid."
                ) from None
            admin_role = roles.get_by_name("Admin")
            if admin_role is None:
                admin_role = Role(name="Admin", description="Platform administration role")
                roles.add(admin_role)
            if roles.get_by_name("User") is None:
                roles.add(Role(name="User", description="Standard platform user role"))
            session.flush()
            user = User(
                username=username,
                display_name=display_name,
                email=email,
                password_hash=password_hash,
                role_id=admin_role.id,
                is_active=True,
                must_change_password=False,
                failed_login_count=0,
                locked_until=None,
                last_login_at=None,
                password_changed_at=now,
                created_at=now,
                created_by=None,
                updated_at=now,
            )
            users.add(user)
            session.flush()
            user_id = user.id
        assert user_id is not None
        return user_id
