"""Shared foundation test fixtures."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from ipsp.config.settings import Environment, Settings
from ipsp.main import create_app

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Return isolated settings without mounting the repository frontend."""
    return Settings(
        _env_file=None,
        environment=Environment.TEST,
        data_dir=tmp_path / "data",
        artifacts_dir=tmp_path / "artifacts",
        log_dir=tmp_path / "logs",
        frontend_dir=tmp_path / "missing-frontend",
        database={"url": f"sqlite:///{(tmp_path / 'control-plane.db').as_posix()}"},
    )


@pytest.fixture
def client(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """Return a test client that surfaces API responses rather than server exceptions."""
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    app = create_app(settings)
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    app.state.foundation_services.database_engine.dispose()
