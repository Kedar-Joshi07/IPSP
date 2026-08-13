"""Phase 1K cross-layer foundation integration proofs."""

from __future__ import annotations

import json
import socket
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from threading import Event
from threading import enumerate as enumerate_threads

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from ipsp.cli.admin import bootstrap_first_admin
from ipsp.config.settings import Environment, Settings
from ipsp.database.models import (
    AuditEvent,
    Permission,
    Role,
    RolePermission,
    User,
    UserSession,
)
from ipsp.errors.exceptions import IPSPError
from ipsp.jobs.contracts import JobExecutionContext, JobProgress
from ipsp.jobs.enums import JobType
from ipsp.main import create_app
from ipsp.repositories.jobs import JobRepository
from ipsp.security.outbound import OutboundAction, OutboundRequest
from sqlalchemy import func, select

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND = PROJECT_ROOT / "frontend"
PASSWORD = "PHASE1K_PASSWORD_DO_NOT_LEAK"
METADATA_MARKER = "PHASE1K_METADATA_DO_NOT_LEAK"


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        _env_file=None,
        environment=Environment.TEST,
        data_dir=tmp_path / "data",
        artifacts_dir=tmp_path / "artifacts",
        log_dir=tmp_path / "logs",
        frontend_dir=FRONTEND,
        database={"url": f"sqlite:///{(tmp_path / 'phase1k.db').as_posix()}"},
    )


def _upgrade(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")


def _add_user(app: object, username: str) -> int:
    services = app.state.foundation_services  # type: ignore[attr-defined]
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
        session.add(user)
        session.flush()
        assert user.id is not None
        return user.id


def _login(client: TestClient, username: str, *, headers: dict[str, str] | None = None):
    return client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": PASSWORD},
        headers=headers,
    )


def test_fresh_database_startup_migration_and_repeated_worker_lifecycle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = _settings(tmp_path)
    app = create_app(settings)
    services = app.state.foundation_services
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            live = client.get("/health/live")
            ready = client.get("/health/ready")
            assert client.get("/").status_code == 200
            assert client.get("/api/v1").status_code == 200
            assert services.job_backend.health().running is False
        assert live.status_code == 200
        assert set(live.json()) == {"status", "timestamp_utc"}
        assert ready.status_code == 503
        assert ready.json()["error_code"] == "SYS-MIGRATION-REQUIRED"
        assert ready.json()["checks"]["job_worker"] == "not_checked"
        assert "phase1k.db" not in ready.text
        assert settings.database.url not in ready.text
    finally:
        services.database_engine.dispose()

    _upgrade(settings, monkeypatch)
    migrated_app = create_app(settings)
    migrated_services = migrated_app.state.foundation_services
    try:
        for _ in range(2):
            with TestClient(migrated_app, raise_server_exceptions=False) as client:
                ready = client.get("/health/ready")
                assert ready.status_code == 200
                assert ready.json()["checks"] == {
                    "application": "ready",
                    "configuration": "ready",
                    "database": "ready",
                    "foreign_keys": "ready",
                    "migration": "ready",
                    "runtime_logs": "ready",
                    "job_worker": "ready",
                }
                assert ready.json()["deferred_checks"] == ["analytical_storage"]
                assert migrated_services.job_backend.health().running is True
            assert migrated_services.job_backend.health().running is False
            assert not any(
                thread.is_alive() and not thread.daemon and thread.name.startswith("ipsp-job-")
                for thread in enumerate_threads()
            )
    finally:
        migrated_services.job_backend.shutdown()
        migrated_services.database_engine.dispose()


def test_bootstrapped_authenticated_offline_job_health_audit_journey(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = _settings(tmp_path)
    _upgrade(settings, monkeypatch)

    def no_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Phase 1 foundation attempted a network operation")

    monkeypatch.setattr(socket, "create_connection", no_network)
    monkeypatch.setattr(socket, "getaddrinfo", no_network)
    monkeypatch.setattr(urllib.request, "urlopen", no_network)

    entered = Event()
    release = Event()
    persisted = Event()

    def handler(context: JobExecutionContext) -> None:
        entered.set()
        assert release.wait(2)
        context.update_progress(JobProgress(75, "verification", "Foundation proof running."))
        context.add_artifact_reference("phase1k/foundation-result.json")

    original_mark_succeeded = JobRepository.mark_succeeded

    def observed_mark_succeeded(repository: JobRepository, job_id: str, now: datetime) -> bool:
        result = original_mark_succeeded(repository, job_id, now)
        persisted.set()
        return result

    monkeypatch.setattr(JobRepository, "mark_succeeded", observed_mark_succeeded)
    app = create_app(settings, job_handlers={JobType.PROFILING: handler})
    services = app.state.foundation_services
    try:
        admin_id = bootstrap_first_admin(
            services.auth_service,
            services.migration_state,
            username="phase1k-admin",
            display_name="Phase 1K Admin",
            email=None,
            password=PASSWORD,
        )
        _add_user(app, "phase1k-user")
        with pytest.raises(IPSPError) as second_bootstrap:
            bootstrap_first_admin(
                services.auth_service,
                services.migration_state,
                username="second-admin",
                display_name="Second Admin",
                email=None,
                password=PASSWORD,
            )
        assert second_bootstrap.value.error_code == "AUTH-BOOTSTRAP_UNAVAILABLE"
        assert PASSWORD not in str(second_bootstrap.value)

        with services.database_sessions.session() as session:
            admin = session.get(User, admin_id)
            assert admin is not None and admin.is_active
            role = session.get(Role, admin.role_id)
            assert role is not None and role.name == "Admin"
            assert admin.password_hash.startswith("$argon2id$")
            assert PASSWORD not in admin.password_hash
            assert session.scalar(select(func.count()).select_from(Permission)) == 13
            assert session.scalar(select(func.count()).select_from(RolePermission)) == 13
            assert (
                session.scalar(
                    select(func.count())
                    .select_from(AuditEvent)
                    .where(AuditEvent.action == "auth.bootstrap_admin")
                )
                == 1
            )

        trace_id = "phase1k-login-trace"
        request_id = "phase1k-login-request"
        with (
            TestClient(app, base_url="https://testserver", raise_server_exceptions=False) as admin,
            TestClient(app, base_url="https://testserver", raise_server_exceptions=False) as user,
        ):
            login = _login(
                admin,
                "phase1k-admin",
                headers={"X-Trace-ID": trace_id, "X-Request-ID": request_id},
            )
            assert login.status_code == 200
            assert login.headers["X-Trace-ID"] == trace_id
            assert login.headers["X-Request-ID"] == request_id
            assert {"password", "token", "csrf"}.isdisjoint(login.json())
            set_cookies = login.headers.get_list("set-cookie")
            assert any("ipsp_session=" in value and "HttpOnly" in value for value in set_cookies)
            assert any("ipsp_csrf=" in value and "HttpOnly" not in value for value in set_cookies)
            assert all("Secure" in value and "SameSite=lax" in value for value in set_cookies)
            raw_session = admin.cookies.get(settings.auth.session_cookie_name)
            raw_csrf = admin.cookies.get(settings.auth.csrf_cookie_name)
            assert raw_session and raw_csrf and raw_session != raw_csrf
            assert raw_session not in login.text and raw_csrf not in login.text

            assert admin.get("/api/v1/auth/me").status_code == 200
            assert admin.get("/health/ready").status_code == 200
            assert admin.get("/api/v1/admin/system/health").status_code == 200

            snapshot = services.job_service.submit(
                JobType.PROFILING,
                admin_id,
                metadata={"private_marker": METADATA_MARKER},
            )
            assert entered.wait(2)
            running = admin.get(f"/api/v1/jobs/{snapshot.job_id}")
            assert running.status_code == 200
            assert running.json()["status"] == "RUNNING"
            assert snapshot.job_id in {
                item["job_id"] for item in admin.get("/api/v1/jobs").json()["jobs"]
            }
            assert METADATA_MARKER not in running.text

            assert _login(user, "phase1k-user").status_code == 200
            hidden = user.get(f"/api/v1/jobs/{snapshot.job_id}")
            absent = user.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000")
            assert hidden.status_code == absent.status_code == 404
            assert hidden.json()["error_code"] == absent.json()["error_code"]

            release.set()
            assert persisted.wait(2)
            completed = admin.get(f"/api/v1/jobs/{snapshot.job_id}")
            assert completed.status_code == 200
            assert completed.json()["status"] == "SUCCEEDED"
            assert completed.json()["progress"] == {
                "percent": 100,
                "phase": "completed",
                "message": "Completed.",
            }
            assert completed.json()["artifact_refs"] == ["phase1k/foundation-result.json"]
            assert services.job_backend.health().running is True

            denial = services.outbound_policy.evaluate(
                OutboundRequest(action=OutboundAction.OTHER_INTERNET)
            )
            assert denial.allowed is False
            assert denial.reason is not None and denial.reason.value == "internet_disabled"

            csrf = admin.cookies.get(settings.auth.csrf_cookie_name)
            assert csrf
            logout = admin.post(
                "/api/v1/auth/logout",
                headers={settings.auth.csrf_header_name: csrf},
            )
            assert logout.status_code == 204
            admin.cookies.set(settings.auth.session_cookie_name, raw_session)
            assert admin.get("/api/v1/auth/me").status_code == 401

        with services.database_sessions.session() as session:
            stored_session = session.scalar(
                select(UserSession).where(UserSession.user_id == admin_id).order_by(UserSession.id)
            )
            assert stored_session is not None
            assert stored_session.token_hash not in {raw_session, raw_csrf}
            assert stored_session.csrf_token_hash not in {raw_session, raw_csrf}
            assert stored_session.invalidated_at is not None
            login_audit = session.scalar(
                select(AuditEvent).where(
                    AuditEvent.action == "auth.login",
                    AuditEvent.status == "success",
                    AuditEvent.user_id == admin_id,
                )
            )
            assert login_audit is not None
            assert login_audit.trace_id == trace_id
            assert login_audit.request_id == request_id
            assert login_audit.resolved_role == "Admin"
            assert login_audit.session_correlation_id == stored_session.session_correlation_id
            assert (
                session.scalar(
                    select(func.count())
                    .select_from(AuditEvent)
                    .where(
                        AuditEvent.action == "job.submit",
                        AuditEvent.user_id == admin_id,
                    )
                )
                == 1
            )

        runtime_log = (settings.log_dir / "ipsp-runtime.jsonl").read_text(encoding="utf-8")
        events = [json.loads(line) for line in runtime_log.splitlines()]
        assert any(
            event["action"] == "http.request"
            and event["trace_id"] == trace_id
            and event["request_id"] == request_id
            for event in events
        )
        for marker in (PASSWORD, raw_session, raw_csrf, METADATA_MARKER):
            assert marker not in runtime_log
    finally:
        release.set()
        services.job_backend.shutdown()
        services.database_engine.dispose()
