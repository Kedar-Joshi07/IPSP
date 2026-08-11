"""Alembic lifecycle and database-backed readiness integration tests."""

from io import StringIO
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from ipsp.config.settings import Environment, Settings
from ipsp.database.engine import create_database_engine
from ipsp.database.migrations import MigrationStateService, canonical_migrations_path
from ipsp.main import create_app
from sqlalchemy import inspect

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_HEAD = "20260811_01"


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

        command.upgrade(_alembic_config(), "head")
        command.upgrade(_alembic_config(), "head")
        upgraded = state_service.inspect()
        assert upgraded.current_revision == EXPECTED_HEAD
        assert upgraded.at_head is True
        assert inspect(engine).get_table_names() == ["alembic_version"]

        command.check(_alembic_config())
        command.downgrade(_alembic_config(), "base")
        downgraded = state_service.inspect()
        assert downgraded.current_revision is None
        assert downgraded.at_head is False

        command.upgrade(_alembic_config(), "head")
        reupgraded = state_service.inspect()
        assert reupgraded.current_revision == EXPECTED_HEAD
        assert reupgraded.at_head is True
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


def test_readiness_is_not_ready_before_migration(settings: Settings) -> None:
    app = create_app(settings)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            live_response = client.get("/health/live")
            response = client.get("/health/ready")
    finally:
        app.state.foundation_services.database_engine.dispose()

    assert live_response.status_code == 200
    assert live_response.json()["status"] == "alive"
    assert response.status_code == 200
    assert response.json()["status"] == "not_ready"
    assert response.json()["error_code"] == "SYS-MIGRATION-REQUIRED"
    assert response.json()["checks"]["database"] == "ready"
    assert response.json()["checks"]["migration"] == "not_ready"


def test_readiness_reports_safe_database_failure(tmp_path: Path) -> None:
    database_path = tmp_path / "missing-directory" / "control-plane.db"
    settings = Settings(
        _env_file=None,
        environment=Environment.TEST,
        frontend_dir=tmp_path / "missing-frontend",
        database={"url": f"sqlite:///{database_path.as_posix()}"},
    )
    app = create_app(settings)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/health/ready")
    finally:
        app.state.foundation_services.database_engine.dispose()

    assert response.status_code == 200
    assert response.json()["status"] == "not_ready"
    assert response.json()["error_code"] == "SYS-DATABASE-UNAVAILABLE"
    assert database_path.name not in response.text
    assert settings.database.url not in response.text


def test_application_construction_does_not_create_or_migrate_database(settings: Settings) -> None:
    database_path = Path(settings.database.url.removeprefix("sqlite:///"))
    app = create_app(settings)
    try:
        assert not database_path.exists()
    finally:
        app.state.foundation_services.database_engine.dispose()
