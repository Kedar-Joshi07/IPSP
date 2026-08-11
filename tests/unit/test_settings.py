"""Typed nested settings and safe-default behavior."""

import json
from pathlib import Path

import pytest
from ipsp.config.feature_flags import FeatureFlags
from ipsp.config.settings import DatabaseSettings, Environment, OutboundSettings, Settings
from ipsp.security.outbound import RemoteTransmissionLevel
from pydantic import ValidationError
from sqlalchemy.engine import make_url

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_default_configuration_is_offline_and_features_are_disabled() -> None:
    settings = Settings(_env_file=None)

    assert settings.features == FeatureFlags()
    assert settings.outbound.internet_enabled is False
    assert settings.outbound.remote_llm_enabled is False
    assert settings.outbound.model_download_enabled is False
    assert settings.outbound.update_check_enabled is False
    assert settings.outbound.allowed_remote_providers == ()
    assert settings.outbound.default_remote_transmission is RemoteTransmissionLevel.REMOTE_DISABLED
    assert (
        Path(make_url(settings.database.url).database or "").resolve()
        == (PROJECT_ROOT / "database" / "ipsp.db").resolve()
    )


def test_default_database_location_does_not_depend_on_current_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_url = Settings(_env_file=None).database.url

    monkeypatch.chdir(tmp_path)

    assert Settings(_env_file=None).database.url == expected_url


def test_settings_load_canonical_nested_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IPSP_APP_NAME", "Configured IPSP")
    monkeypatch.setenv("IPSP_PORT", "9010")
    monkeypatch.setenv("IPSP_FEATURES__REMOTE_LLM_ENABLED", "true")
    monkeypatch.setenv("IPSP_FEATURES__SDV_ENABLED", "true")
    monkeypatch.setenv("IPSP_OUTBOUND__INTERNET_ENABLED", "true")
    monkeypatch.setenv("IPSP_OUTBOUND__REMOTE_LLM_ENABLED", "true")
    monkeypatch.setenv("IPSP_OUTBOUND__ALLOWED_REMOTE_PROVIDERS", '["provider-a"]')
    monkeypatch.setenv(
        "IPSP_OUTBOUND__DEFAULT_REMOTE_TRANSMISSION",
        "sanitized_schema_only",
    )
    monkeypatch.setenv("IPSP_DATABASE__URL", "sqlite:///./configured.db")
    monkeypatch.setenv("IPSP_DATABASE__ECHO", "true")
    monkeypatch.setenv("IPSP_DATABASE__CONNECTION_TIMEOUT_SECONDS", "7.5")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Configured IPSP"
    assert settings.port == 9010
    assert settings.features.remote_llm_enabled is True
    assert settings.features.sdv_enabled is True
    assert settings.outbound.internet_enabled is True
    assert settings.outbound.remote_llm_enabled is True
    assert settings.outbound.allowed_remote_providers == ("provider-a",)
    assert settings.database.url == "sqlite:///./configured.db"
    assert settings.database.echo is True
    assert settings.database.connection_timeout_seconds == 7.5
    assert (
        settings.outbound.default_remote_transmission
        is RemoteTransmissionLevel.SANITIZED_SCHEMA_ONLY
    )


def test_remote_feature_does_not_enable_outbound_permission() -> None:
    settings = Settings(
        _env_file=None,
        features={"remote_llm_enabled": True},
    )

    assert settings.features.remote_llm_enabled is True
    assert settings.outbound.internet_enabled is False
    assert settings.outbound.remote_llm_enabled is False


def test_malformed_provider_identifier_is_rejected() -> None:
    with pytest.raises(ValidationError, match="Provider identifiers"):
        OutboundSettings(allowed_remote_providers=("Bad Provider",))


def test_unknown_transmission_level_is_rejected() -> None:
    with pytest.raises(ValidationError):
        OutboundSettings(default_remote_transmission="sixth_level")  # type: ignore[arg-type]


def test_unknown_secret_provider_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, secrets={"provider": "unfrozen-provider"})


def test_configuration_snapshot_never_loads_secret_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    marker = "DO_NOT_LEAK_PHASE1B_SECRET"
    monkeypatch.setenv("IPSP_PROVIDER_API_KEY", marker)

    settings = Settings(_env_file=None)
    rendered = json.dumps(settings.safe_snapshot(), sort_keys=True)

    assert marker not in rendered
    assert "PROVIDER_API_KEY" not in rendered


def test_production_debug_fails_closed() -> None:
    with pytest.raises(ValidationError, match="Debug mode must be disabled"):
        Settings(_env_file=None, environment=Environment.PRODUCTION, debug=True)


@pytest.mark.parametrize(
    "url",
    (
        "postgresql://localhost/ipsp",
        "mysql://localhost/ipsp",
        "sqlite+aiosqlite:///./control.db",
        "not-a-database-url",
    ),
)
def test_non_sqlite_or_malformed_database_urls_are_rejected(url: str) -> None:
    with pytest.raises(ValidationError):
        DatabaseSettings(url=url)


def test_database_url_credentials_are_rejected_without_echoing_them() -> None:
    marker = "DO_NOT_LEAK_DATABASE_PASSWORD"
    with pytest.raises(ValidationError) as failure:
        DatabaseSettings(url=f"sqlite://user:{marker}@/control.db")

    assert marker not in str(failure.value)
