"""Typed application, feature, secret-provider, and outbound settings."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ipsp.config.feature_flags import FeatureFlags
from ipsp.security.outbound import RemoteTransmissionLevel
from ipsp.security.secrets import SecretProviderKind, validate_provider_identifier


class Environment(StrEnum):
    """Supported application environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class OutboundSettings(BaseModel):
    """Backend-enforced outbound permissions, independent of feature flags."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    internet_enabled: bool = False
    remote_llm_enabled: bool = False
    allowed_remote_providers: tuple[str, ...] = ()
    model_download_enabled: bool = False
    update_check_enabled: bool = False
    default_remote_transmission: RemoteTransmissionLevel = RemoteTransmissionLevel.REMOTE_DISABLED

    @field_validator("allowed_remote_providers")
    @classmethod
    def validate_allowed_providers(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        validated = tuple(validate_provider_identifier(provider) for provider in value)
        if len(set(validated)) != len(validated):
            raise ValueError("Allowed remote provider identifiers must be unique")
        return validated


class SecretSettings(BaseModel):
    """Non-secret provider selection; secret values never enter Settings."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    provider: SecretProviderKind = SecretProviderKind.ENVIRONMENT


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Single validated source for non-secret IPSP process configuration."""

    model_config = SettingsConfigDict(
        env_prefix="IPSP_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        frozen=True,
    )

    environment: Environment = Environment.DEVELOPMENT
    app_name: str = "IPSP"
    app_version: str = "0.1.0"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    data_dir: Path = Field(default_factory=lambda: _repository_root() / "data")
    artifacts_dir: Path = Field(default_factory=lambda: _repository_root() / "artifacts")
    log_dir: Path = Field(default_factory=lambda: _repository_root() / "logs")
    frontend_dir: Path = Field(default_factory=lambda: _repository_root() / "frontend")
    default_theme: Literal["system", "dark", "light"] = "system"
    features: FeatureFlags = Field(default_factory=FeatureFlags)
    outbound: OutboundSettings = Field(default_factory=OutboundSettings)
    secrets: SecretSettings = Field(default_factory=SecretSettings)

    @model_validator(mode="after")
    def validate_safe_environment(self) -> Self:
        """Reject unsafe process behavior without coupling features to permissions."""
        if self.environment is Environment.PRODUCTION and self.debug:
            raise ValueError("Debug mode must be disabled in production")
        return self

    def safe_snapshot(self) -> dict[str, Any]:
        """Return the complete non-secret configuration for diagnostics or hashing."""
        return self.model_dump(mode="json")
