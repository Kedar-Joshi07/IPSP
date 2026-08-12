"""Alembic lifecycle and database-backed readiness integration tests."""

from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from alembic import command
from alembic.config import Config
from alembic.script.revision import RevisionError
from fastapi.testclient import TestClient
from ipsp.config.settings import Environment, Settings
from ipsp.database.engine import create_database_engine
from ipsp.database.migrations import (
    MigrationStateError,
    MigrationStateService,
    canonical_migrations_path,
)
from ipsp.main import create_app
from ipsp.services.readiness import ReadinessService
from sqlalchemy import create_engine, inspect, text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PRIOR_HEAD = "20260812_04"
EXPECTED_HEAD = "20260812_05"
PRIOR_TABLES = [
    "alembic_version",
    "audit_events",
    "permissions",
    "role_permissions",
    "roles",
    "user_sessions",
    "users",
]
EXPECTED_TABLES = ["alembic_version", "audit_events", "jobs", *PRIOR_TABLES[2:]]


def _alembic_config() -> Config:
    return Config(str(PROJECT_ROOT / "alembic.ini"))


def test_migration_upgrade_current_repeat_and_downgrade(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    engine = create_database_engine(settings.database)
    state_service = MigrationStateService(engine, canonical_migrations_path())
    try:
        initial = state_service.inspect()
        assert initial.current_revision is None
        assert initial.expected_head == EXPECTED_HEAD
        assert initial.at_head is False

        command.upgrade(_alembic_config(), PRIOR_HEAD)
        baseline = state_service.inspect()
        assert baseline.current_revision == PRIOR_HEAD
        assert baseline.at_head is False
        assert inspect(engine).get_table_names() == PRIOR_TABLES

        command.upgrade(_alembic_config(), "head")
        command.upgrade(_alembic_config(), "head")
        upgraded = state_service.inspect()
        assert upgraded.current_revision == EXPECTED_HEAD
        assert upgraded.at_head is True
        assert inspect(engine).get_table_names() == EXPECTED_TABLES

        command.check(_alembic_config())
        command.downgrade(_alembic_config(), PRIOR_HEAD)
        downgraded = state_service.inspect()
        assert downgraded.current_revision == PRIOR_HEAD
        assert downgraded.at_head is False
        assert inspect(engine).get_table_names() == PRIOR_TABLES

        command.upgrade(_alembic_config(), "head")
        reupgraded = state_service.inspect()
        assert reupgraded.current_revision == EXPECTED_HEAD
        assert reupgraded.at_head is True
        assert inspect(engine).get_table_names() == EXPECTED_TABLES
    finally:
        engine.dispose()


def test_offline_migration_renders_without_creating_database(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_path = Path(settings.database.url.removeprefix("sqlite:///"))
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    config = _alembic_config()
    output = StringIO()
    config.output_buffer = output

    command.upgrade(config, "head", sql=True)

    assert EXPECTED_HEAD in output.getvalue()
    assert not database_path.exists()


def test_readiness_requires_phase1h_head(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(_alembic_config(), PRIOR_HEAD)
    app = create_app(settings)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            live_response = client.get("/health/live")
            response = client.get("/health/ready")
    finally:
        app.state.foundation_services.database_engine.dispose()

    assert live_response.status_code == 200
    assert live_response.json()["status"] == "alive"
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["error_code"] == "SYS-MIGRATION-REQUIRED"
    assert response.json()["checks"]["database"] == "ready"
    assert response.json()["checks"]["migration"] == "not_ready"


def test_readiness_reports_safe_database_failure(tmp_path: Path) -> None:
    database_path = tmp_path / "missing-directory" / "control-plane.db"
    settings = Settings(
        _env_file=None,
        environment=Environment.TEST,
        log_dir=tmp_path / "logs",
        frontend_dir=tmp_path / "missing-frontend",
        database={"url": f"sqlite:///{database_path.as_posix()}"},
    )
    app = create_app(settings)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            live_response = client.get("/health/live")
            response = client.get("/health/ready")
    finally:
        app.state.foundation_services.database_engine.dispose()

    assert live_response.status_code == 200
    assert live_response.json()["status"] == "alive"
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["error_code"] == "SYS-DATABASE-UNAVAILABLE"
    assert database_path.name not in response.text
    assert settings.database.url not in response.text


def test_readiness_rejects_connection_without_foreign_key_enforcement(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(_alembic_config(), "head")
    unsafe_engine = create_engine(settings.database.url, hide_parameters=True)
    app = create_app(settings)
    readiness_service = ReadinessService(
        settings,
        unsafe_engine,
        MigrationStateService(unsafe_engine, canonical_migrations_path()),
        app.state.foundation_services.job_backend,
    )
    original_services = app.state.foundation_services
    app.state.foundation_services = SimpleNamespace(readiness_service=readiness_service)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/health/ready")
    finally:
        unsafe_engine.dispose()
        original_services.database_engine.dispose()

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["error_code"] == "SYS-DATABASE-FK-DISABLED"
    assert response.json()["checks"]["foreign_keys"] == "not_ready"


def test_multiple_database_migration_heads_fail_readiness_safely(settings: Settings) -> None:
    app = create_app(settings)
    engine = app.state.foundation_services.database_engine
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL PRIMARY KEY)")
        )
        connection.execute(
            text("INSERT INTO alembic_version (version_num) VALUES (:head)"),
            [{"head": "unexpected_head_a"}, {"head": "unexpected_head_b"}],
        )
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/health/ready")
    finally:
        engine.dispose()

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["error_code"] == "SYS-MIGRATION-STATE-UNAVAILABLE"
    assert "unexpected_head" not in response.text


def test_multiple_script_heads_raise_safe_migration_state_error(settings: Settings) -> None:
    engine = create_database_engine(settings.database)
    script_directory = MagicMock()
    script_directory.get_heads.return_value = ["head_a", "head_b"]
    try:
        with (
            patch(
                "ipsp.database.migrations.ScriptDirectory.from_config",
                return_value=script_directory,
            ),
            pytest.raises(MigrationStateError, match="exactly one head"),
        ):
            MigrationStateService(engine, canonical_migrations_path()).expected_head()
    finally:
        engine.dispose()


def test_malformed_script_history_raises_safe_migration_state_error(settings: Settings) -> None:
    engine = create_database_engine(settings.database)
    script_directory = MagicMock()
    script_directory.get_heads.side_effect = RevisionError("private revision details")
    try:
        with (
            patch(
                "ipsp.database.migrations.ScriptDirectory.from_config",
                return_value=script_directory,
            ),
            pytest.raises(MigrationStateError) as failure,
        ):
            MigrationStateService(engine, canonical_migrations_path()).expected_head()
    finally:
        engine.dispose()

    assert str(failure.value) == "Migration history is unavailable"
    assert "private revision details" not in str(failure.value)


def test_application_construction_does_not_create_or_migrate_database(settings: Settings) -> None:
    database_path = Path(settings.database.url.removeprefix("sqlite:///"))
    app = create_app(settings)
    try:
        assert not database_path.exists()
    finally:
        app.state.foundation_services.database_engine.dispose()
