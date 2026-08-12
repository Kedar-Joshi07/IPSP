"""Phase 1I readiness, authorization, diagnostics, and privacy tests."""

from __future__ import annotations

import json
import socket
from dataclasses import asdict, replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ipsp.auth.rbac import CorePermission
from ipsp.config.feature_flags import FeatureFlags
from ipsp.config.settings import DatabaseSettings, OutboundSettings, Settings
from ipsp.database.engine import create_database_engine
from ipsp.database.migrations import (
    MigrationStateError,
    MigrationStateService,
    canonical_migrations_path,
)
from ipsp.database.models import JobRecord, Permission, Role, RolePermission, User
from ipsp.errors.exceptions import IPSPError
from ipsp.jobs.enums import JobStatus, JobType
from ipsp.main import create_app
from ipsp.observability.logging import RUNTIME_LOG_NAME
from ipsp.services.readiness import ReadinessService
from ipsp.services.system_health import MAX_CRITICAL_ERRORS, SystemHealthService
from sqlalchemy import select

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PASSWORD = "health-test-password-秘密"


def _upgrade(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")


def _add_user(app: FastAPI, username: str, role_id: int) -> int:
    services = app.state.foundation_services
    now = datetime.now(UTC)
    with services.database_sessions.transaction() as session:
        user = User(
            username=username,
            display_name=username.title(),
            email=None,
            password_hash=services.password_service.hash(PASSWORD),
            role_id=role_id,
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
        return user.id


def _role_id(app: FastAPI, name: str) -> int:
    with app.state.foundation_services.database_sessions.session() as session:
        role = session.scalar(select(Role).where(Role.name == name))
        assert role is not None
        return role.id


def _login(client: TestClient, username: str) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": PASSWORD},
    )
    assert response.status_code == 200


def _job_record(
    *,
    status: JobStatus,
    updated_at: datetime,
    error_code: str | None = None,
) -> JobRecord:
    return JobRecord(
        job_id=str(uuid4()),
        job_type=JobType.BACKUP.value,
        status=status.value,
        progress_percent=100 if status is JobStatus.SUCCEEDED else 0,
        progress_phase="completed" if status is JobStatus.SUCCEEDED else "finished",
        progress_message="Completed." if status is JobStatus.SUCCEEDED else "Finished.",
        owner_user_id=None,
        trace_id=str(uuid4()),
        request_id=str(uuid4()),
        attempt_count=1,
        max_attempts=1,
        retryable=False,
        cancel_requested=False,
        error_code=error_code,
        error_message="Job execution failed." if error_code else None,
        artifact_refs_json="[]",
        metadata_json="{}",
        created_at=updated_at,
        queued_at=updated_at,
        started_at=updated_at,
        finished_at=updated_at,
        updated_at=updated_at,
    )


def test_health_surfaces_are_separate_and_admin_authority_is_permission_based(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    services.auth_service.bootstrap_admin("named-admin", "Named Admin", None, PASSWORD)
    user_role_id = _role_id(app, "User")
    regular_user_id = _add_user(app, "ordinary-health-user", user_role_id)
    with services.database_sessions.transaction() as session:
        diagnostic_role = Role(name="DiagnosticsOperator", description=None)
        session.add(diagnostic_role)
        session.flush()
        permission = session.scalar(
            select(Permission).where(Permission.code == CorePermission.SYSTEM_CONFIGURE.value)
        )
        assert permission is not None
        session.add(RolePermission(role_id=diagnostic_role.id, permission_id=permission.id))
        diagnostic_role_id = diagnostic_role.id
    diagnostic_user_id = _add_user(app, "diagnostic-health-user", diagnostic_role_id)
    assert regular_user_id != diagnostic_user_id
    assert services.rbac_service.replace_role_permissions(_role_id(app, "Admin"), set())

    rich_only_terms = {
        "free_bytes",
        "database_size_bytes",
        "integrity_status",
        "queue_depth",
        "outbound_policy",
        "local_llm",
        "remote_llm",
        "backup",
        "recent_critical_errors",
        "display_path",
        "logical_cpu_count",
        "process_memory_bytes",
    }
    try:
        with TestClient(
            app, base_url="https://testserver", raise_server_exceptions=False
        ) as client:
            live = client.get("/health/live")
            ready = client.get("/health/ready")
            anonymous = client.get("/api/v1/admin/system/health")
            assert live.status_code == ready.status_code == 200
            assert anonymous.status_code == 401
            assert live.json() == {
                "status": "alive",
                "timestamp_utc": live.json()["timestamp_utc"],
            }
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
            public_text = live.text + ready.text
            assert all(term not in public_text for term in rich_only_terms)

            _login(client, "ordinary-health-user")
            assert client.get("/api/v1/admin/system/health").status_code == 403

            _login(client, "diagnostic-health-user")
            rich = client.get("/api/v1/admin/system/health")
            assert rich.status_code == 200
            body = rich.json()
            assert body["status"] == "healthy"
            assert body["database"] == {
                "status": "healthy",
                "connectivity": True,
                "foreign_keys_enabled": True,
                "migration_at_head": True,
                "integrity_status": "ok",
                "database_size_bytes": body["database"]["database_size_bytes"],
            }
            assert body["database"]["database_size_bytes"] >= 0
            assert body["job_worker"]["running"] is True
            assert body["job_worker"]["accepting_jobs"] is True
            assert body["job_worker"]["worker_count"] == 2
            assert body["job_worker"]["queue_depth"] == 0
            assert body["job_worker"]["persisted_queued_jobs"] == 0
            storage = {item["name"]: item for item in body["storage"]}
            assert storage["logs"]["status"] == "healthy"
            assert storage["logs"]["required_now"] is True
            assert storage["data"]["status"] == "not_initialized"
            assert storage["artifacts"]["status"] == "not_initialized"
            assert storage["data"]["required_now"] is False
            assert storage["artifacts"]["required_now"] is False
            assert storage["logs"]["free_bytes"] >= 0
            assert str(settings.log_dir.parent) not in rich.text
            assert body["local_llm"] == {
                "feature_enabled": False,
                "configured": False,
                "status": "not_implemented",
                "reachable": None,
            }
            assert body["remote_llm"]["reachability_status"] == "policy_disabled"
            assert body["outbound_policy"] == {
                "internet_enabled": False,
                "remote_llm_enabled": False,
                "model_download_enabled": False,
                "update_check_enabled": False,
                "default_remote_transmission": "remote_disabled",
                "allowed_remote_provider_count": 0,
            }
            assert body["model_artifacts"] == {
                "status": "not_initialized",
                "storage_accessible": False,
                "display_path": settings.artifacts_dir.name,
            }
            assert body["backup"]["status"] == "never_run"
            assert (
                body["runtime"]["logical_cpu_count"] is None
                or body["runtime"]["logical_cpu_count"] > 0
            )

            _login(client, "named-admin")
            assert client.get("/api/v1/admin/system/health").status_code == 403
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_full_readiness_requires_worker_and_required_log_storage(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    try:
        stopped = services.readiness_service.check()
        assert stopped.ready is False
        assert stopped.error_code == "SYS-JOB-WORKER-NOT-READY"
        assert stopped.checks["job_worker"] == "not_ready"

        bad_log_path = tmp_path / "DO_NOT_LEAK_HEALTH_LOG_PATH"
        bad_log_path.write_text("not a directory", encoding="utf-8")
        bad_settings = settings.model_copy(update={"log_dir": bad_log_path})
        bad_readiness = ReadinessService(
            bad_settings,
            services.database_engine,
            services.migration_state,
            services.job_backend,
        )
        app.state.foundation_services = replace(services, readiness_service=bad_readiness)
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/health/ready")
        assert response.status_code == 503
        assert response.json()["error_code"] == "SYS-STORAGE-UNAVAILABLE"
        assert response.json()["checks"]["runtime_logs"] == "not_ready"
        assert str(bad_log_path) not in response.text
        assert bad_log_path.name not in response.text
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_worker_start_failure_keeps_liveness_and_admin_diagnostics_available(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    services.auth_service.bootstrap_admin("health-admin", "Health Admin", None, PASSWORD)
    marker = "DO_NOT_LEAK_HEALTH_WORKER_ERROR"

    def fail_start() -> None:
        raise IPSPError("JOB-WORKER-UNAVAILABLE", marker)

    monkeypatch.setattr(services.job_backend, "start", fail_start)
    try:
        with TestClient(
            app, base_url="https://testserver", raise_server_exceptions=False
        ) as client:
            assert client.get("/health/live").status_code == 200
            ready = client.get("/health/ready")
            assert ready.status_code == 503
            assert ready.json()["error_code"] == "SYS-JOB-WORKER-NOT-READY"
            _login(client, "health-admin")
            rich = client.get("/api/v1/admin/system/health")
            assert rich.status_code == 200
            assert rich.json()["status"] == "unhealthy"
            assert rich.json()["job_worker"]["status"] == "unhealthy"
            assert rich.json()["job_worker"]["running"] is False
            assert marker not in rich.text + ready.text
    finally:
        services.database_engine.dispose()


def test_sqlite_and_storage_failures_are_sanitized_in_authorized_health(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    services.auth_service.bootstrap_admin("safe-health-admin", "Safe Health", None, PASSWORD)
    private_database_path = (
        tmp_path / "DO_NOT_LEAK_HEALTH_DB_PATH" / "DO_NOT_LEAK_HEALTH_ERROR_MESSAGE.db"
    )
    broken_settings = settings.model_copy(
        update={"database": DatabaseSettings(url=f"sqlite:///{private_database_path.as_posix()}")}
    )
    broken_engine = create_database_engine(broken_settings.database)
    broken_migrations = MigrationStateService(broken_engine, canonical_migrations_path())
    broken_health = SystemHealthService(
        broken_settings,
        broken_engine,
        services.database_sessions,
        broken_migrations,
        services.readiness_service,
        services.job_backend,
        services.outbound_policy,
    )
    app.state.foundation_services = replace(services, system_health_service=broken_health)
    try:
        with TestClient(
            app, base_url="https://testserver", raise_server_exceptions=False
        ) as client:
            _login(client, "safe-health-admin")
            response = client.get("/api/v1/admin/system/health")
        assert response.status_code == 200
        assert response.json()["status"] == "unhealthy"
        assert response.json()["database"] == {
            "status": "unhealthy",
            "connectivity": False,
            "foreign_keys_enabled": None,
            "migration_at_head": None,
            "integrity_status": "not_available",
            "database_size_bytes": None,
        }
        rendered = response.text
        assert settings.database.url not in rendered
        assert broken_settings.database.url not in rendered
        assert str(tmp_path) not in rendered
        assert "DO_NOT_LEAK_HEALTH" not in rendered
        assert "SELECT 1" not in rendered
    finally:
        services.job_backend.shutdown()
        broken_engine.dispose()
        services.database_engine.dispose()


def test_critical_error_summary_is_bounded_and_excludes_raw_log_content(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    services.auth_service.bootstrap_admin("log-health-admin", "Log Health", None, PASSWORD)
    marker = "DO_NOT_LEAK_HEALTH_LOG_METADATA"
    timestamp = datetime.now(UTC).isoformat()
    lines = ["not-json"]
    lines.append(
        json.dumps(
            {
                "timestamp_utc": timestamp,
                "event_id": str(uuid4()),
                "trace_id": "safe-info-trace",
                "component": "system",
                "action": "system.info",
                "severity": "INFO",
            }
        )
    )
    for index in range(12):
        lines.append(
            json.dumps(
                {
                    "timestamp_utc": timestamp,
                    "event_id": str(uuid4()),
                    "trace_id": f"critical-trace-{index}",
                    "component": "system",
                    "action": "system.critical",
                    "severity": "CRITICAL",
                    "error_code": "SYS-CRITICAL",
                    "message": marker,
                    "metadata": {"password": marker, "path": str(settings.log_dir)},
                }
            )
        )
    rotated = settings.log_dir / f"{RUNTIME_LOG_NAME}.1"
    rotated.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        with TestClient(
            app, base_url="https://testserver", raise_server_exceptions=False
        ) as client:
            _login(client, "log-health-admin")
            response = client.get("/api/v1/admin/system/health")
            assert marker not in client.get("/health/ready").text
        assert response.status_code == 200
        critical = response.json()["recent_critical_errors"]
        assert critical["status"] == "healthy"
        assert critical["maximum_entries"] == MAX_CRITICAL_ERRORS
        assert len(critical["entries"]) == MAX_CRITICAL_ERRORS
        assert all(
            set(entry)
            == {"timestamp_utc", "event_id", "trace_id", "component", "action", "error_code"}
            for entry in critical["entries"]
        )
        assert all(entry["error_code"] == "SYS-CRITICAL" for entry in critical["entries"])
        assert marker not in response.text
        assert str(settings.log_dir) not in response.text
        assert "not-json" not in response.text
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_latest_backup_summary_is_deterministic_and_minimal(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    try:
        assert services.system_health_service.check().backup.status == "never_run"
        now = datetime.now(UTC)
        failed = _job_record(
            status=JobStatus.FAILED,
            updated_at=now,
            error_code="JOB-EXECUTION-FAILED",
        )
        with services.database_sessions.transaction() as session:
            session.add(failed)
        latest_failed = services.system_health_service.check().backup
        assert latest_failed.status == "failed"
        assert latest_failed.job_id == failed.job_id
        assert latest_failed.error_code == "JOB-EXECUTION-FAILED"

        succeeded = _job_record(status=JobStatus.SUCCEEDED, updated_at=now + timedelta(seconds=1))
        succeeded.metadata_json = json.dumps({"password": "DO_NOT_LEAK_HEALTH_SECRET"})
        succeeded.artifact_refs_json = json.dumps(["DO_NOT_LEAK_HEALTH_ARTIFACT"])
        with services.database_sessions.transaction() as session:
            session.add(succeeded)
        latest_succeeded = services.system_health_service.check().backup
        assert latest_succeeded.status == "succeeded"
        assert latest_succeeded.job_id == succeeded.job_id
        assert latest_succeeded.error_code is None
        assert "DO_NOT_LEAK" not in json.dumps(asdict(latest_succeeded), default=str)
    finally:
        services.database_engine.dispose()


def test_enabled_llm_and_outbound_diagnostics_remain_non_networked_and_honest(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    enabled = settings.model_copy(
        update={
            "features": FeatureFlags(local_llm_enabled=True, remote_llm_enabled=True),
            "outbound": OutboundSettings(
                internet_enabled=True,
                remote_llm_enabled=True,
                allowed_remote_providers=("provider-one", "provider-two"),
                model_download_enabled=True,
                update_check_enabled=True,
                default_remote_transmission="sanitized_schema_only",
            ),
        }
    )
    _upgrade(enabled, monkeypatch)
    app = create_app(enabled)
    services = app.state.foundation_services
    try:
        services.job_backend.start()
        with patch.object(socket, "create_connection") as network_call:
            snapshot = services.system_health_service.check()
        network_call.assert_not_called()
        assert snapshot.local_llm.feature_enabled is True
        assert snapshot.local_llm.configured is False
        assert snapshot.local_llm.status == "not_implemented"
        assert snapshot.remote_llm.feature_enabled is True
        assert snapshot.remote_llm.configured is False
        assert snapshot.remote_llm.status == "not_implemented"
        assert snapshot.remote_llm.reachability_status == "not_implemented"
        assert snapshot.remote_llm.allowed_provider_count == 2
        assert snapshot.outbound_policy == snapshot.outbound_policy.__class__(
            internet_enabled=True,
            remote_llm_enabled=True,
            model_download_enabled=True,
            update_check_enabled=True,
            default_remote_transmission="sanitized_schema_only",
            allowed_remote_provider_count=2,
        )
        rendered = json.dumps(asdict(snapshot.remote_llm), default=str)
        assert "provider-one" not in rendered
        assert "provider-two" not in rendered
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()


def test_database_integrity_and_migration_probe_failures_map_to_safe_states(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _upgrade(settings, monkeypatch)
    app = create_app(settings)
    services = app.state.foundation_services
    try:
        services.job_backend.start()
        migration_state = services.migration_state.inspect()
        with (
            patch.object(
                services.system_health_service._engine,
                "connect",  # noqa: SLF001
            ) as connect,
            patch.object(services.migration_state, "inspect", return_value=migration_state),
        ):
            connection = connect.return_value.__enter__.return_value
            connection.execute.return_value = None
            connection.scalar.side_effect = [1, "DO_NOT_LEAK_HEALTH_INTEGRITY_DETAIL", 1, 4096]
            failed_integrity = services.system_health_service._database_diagnostics()  # noqa: SLF001
        assert failed_integrity.connectivity is True
        assert failed_integrity.integrity_status == "failed"
        assert failed_integrity.status == "unhealthy"
        assert "DO_NOT_LEAK" not in json.dumps(asdict(failed_integrity), default=str)

        with patch.object(
            services.migration_state,
            "inspect",
            side_effect=MigrationStateError("DO_NOT_LEAK_HEALTH_MIGRATION_ERROR"),
        ):
            migration_unavailable = services.system_health_service._database_diagnostics()  # noqa: SLF001
        assert migration_unavailable.connectivity is True
        assert migration_unavailable.migration_at_head is None
        assert migration_unavailable.status == "unhealthy"
        assert "DO_NOT_LEAK" not in json.dumps(asdict(migration_unavailable), default=str)
    finally:
        services.job_backend.shutdown()
        services.database_engine.dispose()
