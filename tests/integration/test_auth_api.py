"""Authentication, opaque session, CSRF, lockout, and bootstrap integration tests."""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated

import pytest
from alembic import command
from alembic.config import Config
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from ipsp.api.dependencies.auth import require_authenticated_session
from ipsp.auth.passwords import PasswordService
from ipsp.auth.service import AuthPrincipal
from ipsp.cli.admin import bootstrap_first_admin
from ipsp.cli.admin import main as admin_cli_main
from ipsp.config.settings import Settings
from ipsp.database.models import Role, RolePermission, User, UserSession
from ipsp.errors.exceptions import IPSPError
from ipsp.main import create_app
from sqlalchemy import func, select

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PASSWORD = "test-password-秘密"


@pytest.fixture
def auth_app(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[FastAPI]:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    app = create_app(settings)
    app.state.foundation_services.auth_service.bootstrap_admin(
        "alice", "Alice", "alice@example.test", PASSWORD
    )
    try:
        yield app
    finally:
        app.state.foundation_services.database_engine.dispose()


@pytest.fixture
def auth_client(auth_app: FastAPI) -> Iterator[TestClient]:
    with TestClient(
        auth_app,
        base_url="https://testserver",
        raise_server_exceptions=False,
    ) as client:
        yield client


def _login(client: TestClient, username: str = "alice", password: str = PASSWORD):
    return client.post("/api/v1/auth/login", json={"username": username, "password": password})


def _add_user(app: FastAPI, username: str, *, active: bool = True) -> int:
    services = app.state.foundation_services
    now = datetime.now(UTC)
    with services.database_sessions.transaction() as session:
        role = session.scalar(select(Role).where(Role.name == "User"))
        assert role is not None
        user = User(
            username=username,
            display_name=username.title(),
            email=None,
            password_hash=services.password_service.hash(PASSWORD),
            role_id=role.id,
            is_active=active,
            must_change_password=True,
            failed_login_count=0,
            locked_until=None,
            last_login_at=None,
            password_changed_at=now,
            created_at=now,
            created_by=None,
            updated_at=now,
        )
        session.add(user)
        session.flush()
        return user.id


def test_login_sets_secure_cookies_rotates_and_persists_only_hash(auth_client: TestClient) -> None:
    first = _login(auth_client)
    assert first.status_code == 200
    assert first.headers["cache-control"] == "no-store"
    assert set(first.json()) == {
        "id",
        "username",
        "display_name",
        "email",
        "role_id",
        "role_name",
        "must_change_password",
        "session_correlation_id",
        "session_expires_at",
    }
    assert "password_hash" not in first.json()
    set_cookies = first.headers.get_list("set-cookie")
    session_header = next(value for value in set_cookies if value.startswith("ipsp_session="))
    csrf_header = next(value for value in set_cookies if value.startswith("ipsp_csrf="))
    assert "HttpOnly" in session_header and "Secure" in session_header
    assert "HttpOnly" not in csrf_header and "Secure" in csrf_header
    assert "SameSite=lax" in session_header and "SameSite=lax" in csrf_header

    raw_session = auth_client.cookies.get("ipsp_session")
    raw_csrf = auth_client.cookies.get("ipsp_csrf")
    assert raw_session and raw_csrf and raw_session != raw_csrf
    services = auth_client.app.state.foundation_services
    with services.database_sessions.session() as session:
        persisted = session.scalar(select(UserSession))
        assert persisted is not None
        first_session_id = persisted.id
        assert persisted.token_hash == hashlib.sha256(raw_session.encode()).hexdigest()
        assert persisted.csrf_token_hash == hashlib.sha256(raw_csrf.encode()).hexdigest()
        assert raw_session not in "|".join(str(value) for value in persisted.__dict__.values())
        assert raw_csrf not in "|".join(str(value) for value in persisted.__dict__.values())
        assert persisted.created_at.tzinfo is UTC
        assert persisted.expires_at - persisted.created_at == timedelta(minutes=480)
        assert persisted.session_correlation_id not in {raw_session, persisted.token_hash}

    second = _login(auth_client)
    assert second.status_code == 200
    assert auth_client.cookies.get("ipsp_session") != raw_session
    with services.database_sessions.session() as session:
        old = session.get(UserSession, first_session_id)
        assert old is not None and old.invalidated_at is not None
        assert session.scalar(select(func.count()).select_from(UserSession)) == 2


def test_me_updates_last_seen_and_logout_requires_csrf(auth_client: TestClient) -> None:
    assert _login(auth_client).status_code == 200
    csrf = auth_client.cookies.get("ipsp_csrf")
    services = auth_client.app.state.foundation_services
    token = auth_client.cookies.get("ipsp_session")
    assert csrf and token
    with services.database_sessions.session() as session:
        persisted = session.scalar(
            select(UserSession).where(
                UserSession.token_hash == hashlib.sha256(token.encode()).hexdigest()
            )
        )
        assert persisted is not None
        old_seen = persisted.last_seen_at

    missing = auth_client.post("/api/v1/auth/logout")
    assert missing.status_code == 403
    assert missing.json()["error_code"] == "AUTHZ-CSRF_INVALID"

    me = auth_client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.headers["cache-control"] == "no-store"
    assert "permissions" not in me.json()
    assert "token" not in me.text
    with services.database_sessions.session() as session:
        persisted = session.scalar(
            select(UserSession).where(
                UserSession.token_hash == hashlib.sha256(token.encode()).hexdigest()
            )
        )
        assert persisted is not None and persisted.last_seen_at >= old_seen

    mismatch = auth_client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": f"wrong-{csrf}"})
    assert mismatch.status_code == 403
    logout = auth_client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": csrf})
    assert logout.status_code == 204
    cleared = logout.headers.get_list("set-cookie")
    assert len(cleared) == 2
    assert all("Max-Age=0" in value for value in cleared)
    assert auth_client.get("/api/v1/auth/me").status_code == 401


def test_logout_rejects_present_header_when_csrf_cookie_is_missing(
    auth_client: TestClient,
) -> None:
    settings = auth_client.app.state.settings.auth
    assert _login(auth_client).status_code == 200
    csrf = auth_client.cookies.get(settings.csrf_cookie_name)
    assert csrf
    auth_client.cookies.delete(settings.csrf_cookie_name)

    response = auth_client.post(
        "/api/v1/auth/logout",
        headers={settings.csrf_header_name: csrf},
    )

    assert response.status_code == 403
    assert response.json()["error_code"] == "AUTHZ-CSRF_INVALID"


def test_csrf_from_another_valid_session_cannot_authorize_current_session(
    auth_app: FastAPI,
) -> None:
    settings = auth_app.state.settings.auth
    with (
        TestClient(auth_app, base_url="https://testserver") as first,
        TestClient(auth_app, base_url="https://testserver") as second,
        TestClient(auth_app, base_url="https://testserver") as mixed,
    ):
        assert _login(first).status_code == 200
        assert _login(second).status_code == 200
        first_session = first.cookies.get(settings.session_cookie_name)
        second_csrf = second.cookies.get(settings.csrf_cookie_name)
        assert first_session and second_csrf
        mixed.cookies.set(settings.session_cookie_name, first_session)
        mixed.cookies.set(settings.csrf_cookie_name, second_csrf)

        response = mixed.post(
            "/api/v1/auth/logout",
            headers={settings.csrf_header_name: second_csrf},
        )

        assert response.status_code == 403
        assert response.json()["error_code"] == "AUTHZ-CSRF_INVALID"
        assert first.get("/api/v1/auth/me").status_code == 200


def test_login_replaces_attacker_selected_session_without_persisting_it(
    auth_app: FastAPI,
    caplog: pytest.LogCaptureFixture,
) -> None:
    marker = "ATTACKER_CHOSEN_SESSION_DO_NOT_ACCEPT"
    marker_hash = hashlib.sha256(marker.encode()).hexdigest()
    services = auth_app.state.foundation_services
    cookie_name = auth_app.state.settings.auth.session_cookie_name
    with TestClient(auth_app, base_url="https://testserver") as client:
        client.cookies.set(
            cookie_name,
            marker,
            domain="testserver.local",
            path="/",
        )
        with caplog.at_level(logging.INFO):
            response = _login(client)
        issued_session = client.cookies.get(cookie_name)

    assert response.status_code == 200
    assert issued_session and issued_session != marker
    issued_hash = hashlib.sha256(issued_session.encode()).hexdigest()
    assert issued_hash != marker_hash
    with services.database_sessions.session() as session:
        authenticated = session.scalar(
            select(UserSession).where(UserSession.token_hash == issued_hash)
        )
        attacker_selected = session.scalar(
            select(UserSession).where(UserSession.token_hash == marker_hash)
        )
        assert authenticated is not None
        assert authenticated.token_hash == issued_hash
        assert attacker_selected is None
        persisted_values = "|".join(str(value) for value in authenticated.__dict__.values())
    assert marker not in persisted_values
    assert marker not in response.text
    assert marker not in caplog.text


def test_login_failures_are_generic_and_lockout_expires(auth_app: FastAPI) -> None:
    services = auth_app.state.foundation_services
    _add_user(auth_app, "disabled", active=False)
    with TestClient(
        auth_app, base_url="https://testserver", raise_server_exceptions=False
    ) as client:
        failures = [
            _login(client, "unknown", "wrong"),
            _login(client, "disabled", PASSWORD),
            _login(client, "alice", "wrong"),
        ]
        expected_failure = (
            401,
            "AUTH-INVALID_CREDENTIALS",
            "Authentication failed.",
        )
        for response in failures:
            assert (
                response.status_code,
                response.json()["error_code"],
                response.json()["message"],
            ) == expected_failure

        for _ in range(4):
            assert _login(client, "alice", "wrong").status_code == 401
        locked_response = _login(client)
        assert (
            locked_response.status_code,
            locked_response.json()["error_code"],
            locked_response.json()["message"],
        ) == expected_failure

        with services.database_sessions.transaction() as session:
            alice = session.scalar(select(User).where(User.username == "alice"))
            assert alice is not None
            assert alice.failed_login_count == 5
            assert alice.locked_until is not None
            alice.locked_until = datetime.now(UTC) - timedelta(seconds=1)

        assert _login(client).status_code == 200
        with services.database_sessions.session() as session:
            alice = session.scalar(select(User).where(User.username == "alice"))
            assert alice is not None
            assert alice.failed_login_count == 0
            assert alice.locked_until is None
            assert alice.last_login_at is not None


def test_login_argon2_failure_cost_paths_are_exact(
    auth_app: FastAPI,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    services = auth_app.state.foundation_services
    _add_user(auth_app, "disabled", active=False)
    _add_user(auth_app, "locked")
    with services.database_sessions.transaction() as session:
        locked = session.scalar(select(User).where(User.username == "locked"))
        assert locked is not None
        locked.locked_until = datetime.now(UTC) + timedelta(minutes=5)

    passwords = services.password_service
    dummy_calls: list[str] = []
    real_calls: list[str] = []
    original_dummy = passwords.equalize_unknown_user
    original_real = passwords.verify_and_update

    def observe_dummy(candidate: str) -> None:
        dummy_calls.append(candidate)
        original_dummy(candidate)

    def observe_real(candidate: str, password_hash: str) -> tuple[bool, str | None]:
        real_calls.append(candidate)
        return original_real(candidate, password_hash)

    monkeypatch.setattr(passwords, "equalize_unknown_user", observe_dummy)
    monkeypatch.setattr(passwords, "verify_and_update", observe_real)

    def assert_failure(username: str, password: str) -> None:
        with pytest.raises(IPSPError) as failure:
            services.auth_service.login(username, password)
        assert failure.value.error_code == "AUTH-INVALID_CREDENTIALS"
        assert failure.value.safe_message == "Authentication failed."

    assert_failure("unknown", "unknown-password")
    assert dummy_calls == ["unknown-password"]
    assert real_calls == []

    dummy_calls.clear()
    assert_failure("disabled", PASSWORD)
    assert dummy_calls == [PASSWORD]
    assert real_calls == []

    dummy_calls.clear()
    assert_failure("locked", PASSWORD)
    assert dummy_calls == [PASSWORD]
    assert real_calls == []

    dummy_calls.clear()
    assert_failure("alice", "wrong-password")
    assert dummy_calls == []
    assert real_calls == ["wrong-password"]

    real_calls.clear()
    assert services.auth_service.login("alice", PASSWORD).principal.username == "alice"
    assert dummy_calls == []
    assert real_calls == [PASSWORD]


def test_disabled_authenticated_user_is_rejected_and_session_invalidated(
    auth_client: TestClient,
) -> None:
    assert _login(auth_client).status_code == 200
    services = auth_client.app.state.foundation_services
    with services.database_sessions.transaction() as session:
        alice = session.scalar(select(User).where(User.username == "alice"))
        assert alice is not None
        alice.is_active = False

    response = auth_client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["error_code"] == "AUTH-SESSION_INVALID"
    with services.database_sessions.session() as session:
        persisted = session.scalar(select(UserSession))
        assert persisted is not None and persisted.invalidated_at is not None


def test_unknown_expired_and_explicitly_invalidated_sessions_are_rejected(
    auth_app: FastAPI,
) -> None:
    services = auth_app.state.foundation_services
    with pytest.raises(IPSPError) as unknown:
        services.auth_service.authenticate_session("not-a-real-session")
    assert unknown.value.error_code == "AUTH-SESSION_INVALID"

    start = datetime.now(UTC)
    result = services.auth_service.login("alice", PASSWORD, timestamp=start)
    with pytest.raises(IPSPError) as expired:
        services.auth_service.authenticate_session(
            result.session_token,
            timestamp=result.principal.session_expires_at,
        )
    assert expired.value.error_code == "AUTH-SESSION_INVALID"
    with services.database_sessions.session() as session:
        persisted = session.get(UserSession, result.principal.session_id)
        assert persisted is not None and persisted.invalidated_at is not None

    replacement = services.auth_service.login("alice", PASSWORD, timestamp=start)
    services.auth_service.logout(replacement.principal, timestamp=start)
    with pytest.raises(IPSPError) as invalidated:
        services.auth_service.authenticate_session(replacement.session_token, timestamp=start)
    assert invalidated.value.error_code == "AUTH-SESSION_INVALID"


def test_csrf_stored_hash_mismatch_and_unicode_input_fail_safely(auth_client: TestClient) -> None:
    assert _login(auth_client).status_code == 200
    services = auth_client.app.state.foundation_services
    csrf = auth_client.cookies.get("ipsp_csrf")
    assert csrf
    with services.database_sessions.transaction() as session:
        persisted = session.scalar(select(UserSession).where(UserSession.invalidated_at.is_(None)))
        assert persisted is not None
        persisted.csrf_token_hash = "0" * 64

    mismatch = auth_client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": csrf})
    assert mismatch.status_code == 403
    token = auth_client.cookies.get("ipsp_session")
    assert token
    principal = services.auth_service.authenticate_session(token)
    with pytest.raises(IPSPError) as unicode_failure:
        services.auth_service.validate_csrf(principal, "非ASCII-🔐", "非ASCII-🔐")
    assert unicode_failure.value.error_code == "AUTHZ-CSRF_INVALID"


def test_password_change_invalidates_all_user_sessions_but_not_other_user(
    auth_app: FastAPI,
) -> None:
    bob_id = _add_user(auth_app, "bob")
    services = auth_app.state.foundation_services
    with services.database_sessions.session() as session:
        before_changed_at = session.scalar(
            select(User.password_changed_at).where(User.username == "alice")
        )
    with (
        TestClient(auth_app, base_url="https://testserver") as first,
        TestClient(auth_app, base_url="https://testserver") as second,
        TestClient(auth_app, base_url="https://testserver") as bob,
    ):
        assert _login(first).status_code == 200
        assert _login(second).status_code == 200
        assert _login(bob, "bob").status_code == 200
        csrf = first.cookies.get("ipsp_csrf")
        assert csrf
        changed = first.post(
            "/api/v1/auth/change-password",
            headers={"X-CSRF-Token": csrf},
            json={"current_password": PASSWORD, "new_password": "new-password-🔐"},
        )
        assert changed.status_code == 204
        assert first.get("/api/v1/auth/me").status_code == 401
        assert second.get("/api/v1/auth/me").status_code == 401
        assert bob.get("/api/v1/auth/me").status_code == 200

    with services.database_sessions.session() as session:
        alice = session.scalar(select(User).where(User.username == "alice"))
        assert alice is not None
        assert services.password_service.verify("new-password-🔐", alice.password_hash)
        assert not services.password_service.verify(PASSWORD, alice.password_hash)
        assert alice.must_change_password is False
        assert before_changed_at is not None and alice.password_changed_at > before_changed_at
        bob_active = session.scalar(
            select(func.count())
            .select_from(UserSession)
            .where(UserSession.user_id == bob_id, UserSession.invalidated_at.is_(None))
        )
        assert bob_active == 1


def test_wrong_current_password_is_safe_and_does_not_change_hash(auth_client: TestClient) -> None:
    marker = "DO_NOT_LEAK_LOGIN_PASSWORD"
    assert _login(auth_client).status_code == 200
    services = auth_client.app.state.foundation_services
    with services.database_sessions.session() as session:
        before = session.scalar(select(User.password_hash).where(User.username == "alice"))
    csrf = auth_client.cookies.get("ipsp_csrf")
    response = auth_client.post(
        "/api/v1/auth/change-password",
        headers={"X-CSRF-Token": csrf or ""},
        json={"current_password": marker, "new_password": "not-installed"},
    )
    assert response.status_code == 401
    assert response.json()["error_code"] == "AUTH-PASSWORD_INVALID"
    assert marker not in response.text
    with services.database_sessions.session() as session:
        after = session.scalar(select(User.password_hash).where(User.username == "alice"))
    assert after == before


def test_role_change_invalidation_primitive_is_user_scoped(auth_app: FastAPI) -> None:
    bob_id = _add_user(auth_app, "bob")
    services = auth_app.state.foundation_services
    with (
        TestClient(auth_app, base_url="https://testserver") as alice_one,
        TestClient(auth_app, base_url="https://testserver") as alice_two,
        TestClient(auth_app, base_url="https://testserver") as bob,
    ):
        alice_id = _login(alice_one).json()["id"]
        assert _login(alice_two).status_code == 200
        assert _login(bob, "bob").status_code == 200
        services.auth_service.invalidate_all_user_sessions(alice_id)
        assert alice_one.get("/api/v1/auth/me").status_code == 401
        assert alice_two.get("/api/v1/auth/me").status_code == 401
        assert bob.get("/api/v1/auth/me").status_code == 200
    assert bob_id != alice_id


def test_bootstrap_requires_head_is_one_time_and_creates_core_permissions(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    app = create_app(settings)
    services = app.state.foundation_services
    try:
        user_id = bootstrap_first_admin(
            services.auth_service,
            services.migration_state,
            username="first-admin",
            display_name="First Admin",
            email=None,
            password=PASSWORD,
        )
        with services.database_sessions.session() as session:
            user = session.get(User, user_id)
            assert user is not None
            role = session.get(Role, user.role_id)
            assert role is not None and role.name == "Admin"
            assert {name for (name,) in session.execute(select(Role.name))} == {"Admin", "User"}
            assert session.scalar(select(func.count()).select_from(RolePermission)) == 13
            assert PasswordService().verify(PASSWORD, user.password_hash)
        with pytest.raises(IPSPError, match="no longer available"):
            bootstrap_first_admin(
                services.auth_service,
                services.migration_state,
                username="second",
                display_name="Second",
                email=None,
                password=PASSWORD,
            )
    finally:
        services.database_engine.dispose()


def test_interactive_bootstrap_never_outputs_password(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    marker = "DO_NOT_LEAK_LOGIN_PASSWORD"
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    responses = iter(("cli-admin", "CLI Admin", ""))
    monkeypatch.setattr("builtins.input", lambda _prompt: next(responses))
    monkeypatch.setattr("getpass.getpass", lambda _prompt: marker)

    assert admin_cli_main() == 0

    captured = capsys.readouterr()
    assert marker not in captured.out + captured.err


def test_unknown_user_runs_dummy_verification(
    auth_app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    passwords = auth_app.state.foundation_services.password_service
    calls: list[str] = []
    original = passwords.equalize_unknown_user

    def observe(candidate: str) -> None:
        calls.append(candidate)
        original(candidate)

    monkeypatch.setattr(passwords, "equalize_unknown_user", observe)
    with pytest.raises(IPSPError) as failure:
        auth_app.state.foundation_services.auth_service.login("unknown-user", "unknown-password")
    assert failure.value.error_code == "AUTH-INVALID_CREDENTIALS"
    assert calls == ["unknown-password"]


def test_auth_markers_are_absent_from_logs_and_errors(
    auth_client: TestClient,
    caplog: pytest.LogCaptureFixture,
) -> None:
    markers = {
        "DO_NOT_LEAK_LOGIN_PASSWORD",
        "DO_NOT_LEAK_SESSION_TOKEN",
        "DO_NOT_LEAK_CSRF_TOKEN",
    }
    with caplog.at_level(logging.INFO):
        bad_login = _login(auth_client, password="DO_NOT_LEAK_LOGIN_PASSWORD")
        assert _login(auth_client).status_code == 200
        raw_session = auth_client.cookies.get("ipsp_session")
        raw_csrf = auth_client.cookies.get("ipsp_csrf")
        auth_client.cookies.set("ipsp_csrf", "DO_NOT_LEAK_CSRF_TOKEN")
        bad_csrf = auth_client.post(
            "/api/v1/auth/logout",
            headers={"X-CSRF-Token": "DO_NOT_LEAK_CSRF_TOKEN"},
        )
        auth_client.cookies.set("ipsp_session", "DO_NOT_LEAK_SESSION_TOKEN")
        bad_session = auth_client.get("/api/v1/auth/me")
    rendered = caplog.text + bad_login.text + bad_csrf.text + bad_session.text
    assert raw_session and raw_session not in rendered
    assert raw_csrf and raw_csrf not in rendered
    assert bad_login.status_code == 401
    assert bad_csrf.status_code == 403
    assert bad_session.status_code == 401
    assert all(marker not in rendered for marker in markers)


def test_dependency_populates_safe_request_state(auth_app: FastAPI) -> None:
    @auth_app.get("/test-auth-state")
    def state_probe(
        request: Request,
        principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
    ) -> dict[str, int | str]:
        return {
            "user_id": request.state.user_id,
            "role_id": request.state.role_id,
            "role_name": request.state.role_name,
            "session_correlation_id": request.state.session_correlation_id,
            "principal_correlation_id": principal.session_correlation_id,
        }

    with TestClient(auth_app, base_url="https://testserver") as client:
        correlation_id = _login(client).json()["session_correlation_id"]
        response = client.get("/test-auth-state")
    assert response.status_code == 200
    assert response.json()["session_correlation_id"] == correlation_id
    assert response.json()["principal_correlation_id"] == correlation_id
