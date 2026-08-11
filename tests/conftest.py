"""Shared Phase 1A test fixtures."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from ipsp.config.settings import Environment, Settings
from ipsp.main import create_app


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
    )


@pytest.fixture
def client(settings: Settings) -> TestClient:
    """Return a test client that surfaces API responses rather than server exceptions."""
    return TestClient(create_app(settings), raise_server_exceptions=False)
