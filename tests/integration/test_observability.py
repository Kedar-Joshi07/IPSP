"""Phase 1G durable audit, trace continuity, and privacy integration tests."""

import json
from datetime import UTC, datetime
from pathlib import Path
from threading import Barrier, Thread
from typing import Annotated

import pytest
from alembic import command
from alembic.config import Config
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from ipsp.api.dependencies.auth import require_authenticated_session
from ipsp.api.dependencies.rbac import require_permission
from ipsp.auth.rbac import CorePermission
from ipsp.auth.service import AuthPrincipal
from ipsp.config.settings import Settings
from ipsp.database.models import AuditEvent, Role, User
from ipsp.main import create_app
from ipsp.observability.audit import decode_metadata
from ipsp.observability.context import current_observability_context
from ipsp.observability.events import EventStream
from ipsp.repositories.audit import AuditEventRepository
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PASSWORD = "observability-test-password-秘密"


def _upgrade(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> FastAPI:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    return create_app(settings)


def _audit_events(app: FastAPI) -> list[AuditEvent]:
    with app.state.foundation_services.database_sessions.session() as session:
        events = list(session.scalars(select(AuditEvent).order_by(AuditEvent.id)))
        for event in events:
            session.expunge(event)
        return events


def _current_context_dict() -> dict[str, object]:
    context = current_observability_context()
    return {
        "request_id": context.request_id,
        "trace_id": context.trace_id,
        "session_correlation_id": context.session_correlation_id,
        "user_id": context.user_id,
        "resolved_role": context.resolved_role,
    }


def test_audit_schema_constraints_and_sanitized_metadata(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    marker = "DO_NOT_LEAK_AUDIT_SECRET"
    try:
        event = services.audit_service.record(
            stream=EventStream.SECURITY,
            component="test",
            action="test.persist",
            status="success",
            severity="INFO",
            timestamp_utc=datetime(2026, 8, 12, 12, 0, tzinfo=UTC),
            metadata={"safe": "visible", "password": marker, "csrf_token": marker},
        )
        with services.database_sessions.session() as session:
            persisted = AuditEventRepository(session).get_by_event_id(event.event_id)
            assert persisted is not None
            assert persisted.timestamp_utc == datetime(2026, 8, 12, 12, 0, tzinfo=UTC)
            assert decode_metadata(persisted.metadata_json) == {
                "csrf_token": "[REDACTED]",
                "password": "[REDACTED]",
                "safe": "visible",
            }
            assert AuditEventRepository(session).count() == 1

        database_path = Path(settings.database.url.removeprefix("sqlite:///"))
        assert marker.encode() not in database_path.read_bytes()
        assert {
            "password",
            "password_hash",
            "session_token",
            "csrf_token",
            "token_hash",
            "request_body",
            "headers",
            "authorization",
            "cookie",
        }.isdisjoint(AuditEvent.__table__.columns.keys())

        with pytest.raises(IntegrityError), services.database_sessions.transaction() as session:
            session.add(
                AuditEvent(
                    event_id=event.event_id,
                    timestamp_utc=datetime.now(UTC),
                    stream="security",
                    trace_id="trace",
                    request_id="request",
                    component="test",
                    action="duplicate",
                    status="failure",
                    severity="WARNING",
                    metadata_json="{}",
                )
            )
        with pytest.raises(IntegrityError), services.database_sessions.transaction() as session:
            session.add(
                AuditEvent(
                    event_id="00000000-0000-4000-8000-000000000002",
                    timestamp_utc=datetime.now(UTC),
                    stream="security",
                    trace_id="trace",
                    request_id="request",
                    component="test",
                    action="negative-duration",
                    status="failure",
                    severity="WARNING",
                    duration_ms=-1,
                    metadata_json="{}",
                )
            )
    finally:
        services.database_engine.dispose()


def test_auth_security_actions_are_durable_and_private(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    try:
        user_id = services.auth_service.bootstrap_admin(
            "audit-admin", "Audit Admin", None, PASSWORD
        )
        with TestClient(app, base_url="https://testserver") as client:
            failed_login = client.post(
                "/api/v1/auth/login",
                json={"username": "unknown-sensitive-name", "password": "wrong-password"},
            )
            assert failed_login.status_code == 401
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "audit-admin", "password": PASSWORD},
            )
            assert login.status_code == 200
            csrf = client.cookies.get(settings.auth.csrf_cookie_name)
            assert csrf
            failed_change = client.post(
                "/api/v1/auth/change-password",
                json={"current_password": "wrong-current", "new_password": "unused-password"},
                headers={settings.auth.csrf_header_name: csrf},
            )
            assert failed_change.status_code == 401
            invalid_csrf = client.post(
                "/api/v1/auth/logout",
                headers={settings.auth.csrf_header_name: "DO_NOT_LEAK_CSRF_VALUE"},
            )
            assert invalid_csrf.status_code == 403
            changed = client.post(
                "/api/v1/auth/change-password",
                json={"current_password": PASSWORD, "new_password": "updated-password-秘密"},
                headers={settings.auth.csrf_header_name: csrf},
            )
            assert changed.status_code == 204
            assert (
                client.post(
                    "/api/v1/auth/login",
                    json={"username": "audit-admin", "password": "updated-password-秘密"},
                ).status_code
                == 200
            )
            csrf = client.cookies.get(settings.auth.csrf_cookie_name)
            assert csrf
            assert (
                client.post(
                    "/api/v1/auth/logout",
                    headers={settings.auth.csrf_header_name: csrf},
                ).status_code
                == 204
            )

        actions = [event.action for event in _audit_events(app)]
        assert "auth.bootstrap_admin" in actions
        assert actions.count("auth.login") == 3
        assert "auth.csrf_validation" in actions
        assert "auth.password_change" in actions
        assert actions.count("auth.password_change") == 2
        assert "auth.logout" in actions
        database_path = Path(settings.database.url.removeprefix("sqlite:///"))
        persisted_bytes = database_path.read_bytes()
        for marker in (
            b"unknown-sensitive-name",
            b"wrong-password",
            b"DO_NOT_LEAK_CSRF_VALUE",
            PASSWORD.encode(),
        ):
            assert marker not in persisted_bytes
        assert any(event.user_id == user_id for event in _audit_events(app))
    finally:
        services.database_engine.dispose()


def test_trace_continuity_and_runtime_sqlite_separation(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    try:
        services.auth_service.bootstrap_admin("trace-admin", "Trace Admin", None, PASSWORD)
        permission_dependency = require_permission(CorePermission.USER_MANAGE)

        @app.get("/test-observability-denied")
        def denied(_principal: object = Depends(permission_dependency)) -> dict[str, bool]:
            return {"allowed": True}

        with TestClient(app, base_url="https://testserver") as client:
            assert (
                client.post(
                    "/api/v1/auth/login",
                    json={"username": "trace-admin", "password": PASSWORD},
                ).status_code
                == 200
            )
            principal = services.auth_service.authenticate_session(
                client.cookies.get(settings.auth.session_cookie_name)
            )
            services.rbac_service.replace_role_permissions(principal.role_id, set())
            assert (
                client.post(
                    "/api/v1/auth/login",
                    json={"username": "trace-admin", "password": PASSWORD},
                ).status_code
                == 200
            )
            trace_id = "trace-continuity-123"
            request_id = "request-continuity-123"
            response = client.get(
                "/test-observability-denied",
                headers={"X-Trace-ID": trace_id, "X-Request-ID": request_id},
            )
            assert response.status_code == 403
            assert response.headers["X-Trace-ID"] == trace_id
            assert response.headers["X-Request-ID"] == request_id

        durable = next(
            event
            for event in reversed(_audit_events(app))
            if event.action == "rbac.permission_denied"
        )
        assert durable.trace_id == trace_id
        assert durable.request_id == request_id
        assert durable.session_correlation_id
        assert durable.resolved_role == "Admin"

        runtime_lines = [
            json.loads(line)
            for line in (settings.log_dir / "ipsp-runtime.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        completion = next(
            item
            for item in reversed(runtime_lines)
            if item["action"] == "http.request"
            and item["trace_id"] == trace_id
            and item["request_id"] == request_id
        )
        assert completion["session_correlation_id"] == durable.session_correlation_id
        assert completion["user_id"] == durable.user_id
        assert completion["resolved_role"] == durable.resolved_role

        before = len(_audit_events(app))
        with TestClient(app, base_url="https://testserver") as client:
            assert client.get("/health/live").status_code == 200
        assert len(_audit_events(app)) == before
    finally:
        services.database_engine.dispose()


def test_audit_insert_failure_rolls_back_security_mutation(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    try:
        services.auth_service.bootstrap_admin("rollback-admin", "Rollback Admin", None, PASSWORD)
        principal = services.auth_service.login("rollback-admin", PASSWORD).principal
        original_role_id = principal.role_id
        with services.database_sessions.transaction() as session:
            session.execute(
                text(
                    "CREATE TRIGGER reject_audit BEFORE INSERT ON audit_events "
                    "BEGIN SELECT RAISE(ABORT, 'audit rejected'); END"
                )
            )
        with services.database_sessions.transaction() as session:
            session.execute(text("INSERT INTO roles (name) VALUES ('Other')"))
            other_role_id = int(session.scalar(text("SELECT id FROM roles WHERE name='Other'")))

        with pytest.raises(IntegrityError):
            services.rbac_service.assign_user_role(principal.user_id, other_role_id)

        with services.database_sessions.session() as session:
            role_id = session.scalar(
                text("SELECT role_id FROM users WHERE id=:id"),
                {"id": principal.user_id},
            )
        assert role_id == original_role_id
    finally:
        services.database_engine.dispose()


def test_rbac_mutations_emit_only_actual_change_events(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    try:
        user_id = services.auth_service.bootstrap_admin(
            "mutation-admin", "Mutation Admin", None, PASSWORD
        )
        with services.database_sessions.transaction() as session:
            role = Role(name="MutationRole", description=None)
            session.add(role)
            session.flush()
            role_id = role.id

        before = len(_audit_events(app))
        assert services.rbac_service.assign_user_role(user_id, role_id) is True
        assert services.rbac_service.assign_user_role(user_id, role_id) is False
        assert (
            services.rbac_service.replace_role_permissions(role_id, {CorePermission.DATASET_VIEW})
            is True
        )
        assert (
            services.rbac_service.replace_role_permissions(role_id, {CorePermission.DATASET_VIEW})
            is False
        )

        new_actions = [event.action for event in _audit_events(app)[before:]]
        assert new_actions.count("rbac.user_role_change") == 1
        assert new_actions.count("rbac.role_permissions_change") == 1
    finally:
        services.database_engine.dispose()


def test_authenticated_context_reaches_sync_route_and_downstream_dependency(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    try:
        services.auth_service.bootstrap_admin("context-admin", "Context Admin", None, PASSWORD)

        def downstream(
            _principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
        ) -> dict[str, object]:
            return _current_context_dict()

        @app.get("/test-authenticated-context")
        def authenticated_context(
            principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
            dependency_context: Annotated[dict[str, object], Depends(downstream)],
        ) -> dict[str, object]:
            return {
                "route": _current_context_dict(),
                "dependency": dependency_context,
                "principal_user_id": principal.user_id,
            }

        with TestClient(app, base_url="https://testserver") as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "context-admin", "password": PASSWORD},
            )
            response = client.get(
                "/test-authenticated-context",
                headers={"X-Trace-ID": "context-trace", "X-Request-ID": "context-request"},
            )

        assert response.status_code == 200
        body = response.json()
        expected = {
            "request_id": "context-request",
            "trace_id": "context-trace",
            "session_correlation_id": login.json()["session_correlation_id"],
            "user_id": login.json()["id"],
            "resolved_role": "Admin",
        }
        assert body["route"] == expected
        assert body["dependency"] == expected
        assert body["principal_user_id"] == expected["user_id"]
    finally:
        services.database_engine.dispose()


def test_authenticated_handled_error_log_inherits_identity_and_anonymous_does_not(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    try:
        services.auth_service.bootstrap_admin("error-admin", "Error Admin", None, PASSWORD)

        @app.get("/test-authenticated-error")
        def authenticated_error(
            _principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
        ) -> None:
            from ipsp.errors.exceptions import IPSPError

            raise IPSPError("AUTHZ-TEST", "Permission denied.")

        @app.get("/test-anonymous-context")
        def anonymous_context() -> dict[str, object]:
            return {
                key: value
                for key, value in _current_context_dict().items()
                if key in {"session_correlation_id", "user_id", "resolved_role"}
            }

        with TestClient(app, base_url="https://testserver") as client:
            login = client.post(
                "/api/v1/auth/login",
                json={"username": "error-admin", "password": PASSWORD},
            )
            response = client.get(
                "/test-authenticated-error",
                headers={"X-Trace-ID": "handled-trace", "X-Request-ID": "handled-request"},
            )
            anonymous = client.get("/test-anonymous-context")

        assert response.status_code == 403
        runtime_events = [
            json.loads(line)
            for line in (settings.log_dir / "ipsp-runtime.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        handled = next(
            event
            for event in reversed(runtime_events)
            if event["action"] == "exception.handled" and event["trace_id"] == "handled-trace"
        )
        assert handled["user_id"] == login.json()["id"]
        assert handled["session_correlation_id"] == login.json()["session_correlation_id"]
        assert handled["resolved_role"] == "Admin"
        assert anonymous.json() == {
            "session_correlation_id": None,
            "user_id": None,
            "resolved_role": None,
        }
    finally:
        services.database_engine.dispose()


def test_concurrent_authenticated_requests_do_not_cross_contaminate_context(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = _upgrade(settings, monkeypatch)
    services = app.state.foundation_services
    barrier = Barrier(2)
    try:
        first_id = services.auth_service.bootstrap_admin("first-user", "First User", None, PASSWORD)
        with services.database_sessions.transaction() as session:
            user_role = session.scalar(select(Role).where(Role.name == "User"))
            assert user_role is not None
            now = datetime.now(UTC)
            second = User(
                username="second-user",
                display_name="Second User",
                email=None,
                password_hash=services.password_service.hash(PASSWORD),
                role_id=user_role.id,
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
            session.add(second)
            session.flush()
            second_id = second.id

        @app.get("/test-interleaved-context")
        def interleaved_context(
            _principal: Annotated[AuthPrincipal, Depends(require_authenticated_session)],
        ) -> dict[str, object]:
            before = _current_context_dict()
            barrier.wait()
            return {"before": before, "after": _current_context_dict()}

        results: dict[str, dict[str, object]] = {}

        def request_as(username: str, trace_id: str) -> None:
            with TestClient(app, base_url="https://testserver") as client:
                login = client.post(
                    "/api/v1/auth/login", json={"username": username, "password": PASSWORD}
                )
                assert login.status_code == 200
                response = client.get(
                    "/test-interleaved-context",
                    headers={"X-Trace-ID": trace_id, "X-Request-ID": f"request-{trace_id}"},
                )
                assert response.status_code == 200
                results[username] = {
                    "login": login.json(),
                    "context": response.json(),
                }

        threads = [
            Thread(target=request_as, args=("first-user", "trace-first")),
            Thread(target=request_as, args=("second-user", "trace-second")),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert set(results) == {"first-user", "second-user"}
        for username, user_id, trace_id in (
            ("first-user", first_id, "trace-first"),
            ("second-user", second_id, "trace-second"),
        ):
            login = results[username]["login"]
            contexts = results[username]["context"]
            expected = {
                "request_id": f"request-{trace_id}",
                "trace_id": trace_id,
                "session_correlation_id": login["session_correlation_id"],
                "user_id": user_id,
                "resolved_role": login["role_name"],
            }
            assert contexts == {"before": expected, "after": expected}
    finally:
        services.database_engine.dispose()
