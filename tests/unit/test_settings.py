"""Typed settings behavior."""

import pytest
from ipsp.config.settings import Environment, Settings
from pydantic import ValidationError


def test_settings_load_from_prefixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IPSP_APP_NAME", "Configured IPSP")
    monkeypatch.setenv("IPSP_PORT", "9010")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Configured IPSP"
    assert settings.port == 9010
    assert settings.internet_enabled is False


def test_production_debug_fails_closed() -> None:
    with pytest.raises(ValidationError, match="Debug mode must be disabled"):
        Settings(_env_file=None, environment=Environment.PRODUCTION, debug=True)


def test_remote_access_requires_outbound_policy() -> None:
    with pytest.raises(ValidationError, match="outbound internet policy"):
        Settings(_env_file=None, remote_llm_enabled=True, internet_enabled=False)
