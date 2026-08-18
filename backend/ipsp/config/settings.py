"""Typed application, feature, secret-provider, and outbound settings."""

from __future__ import annotations

import re
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError

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


def _default_database_url() -> str:
    database_path = (_repository_root() / "database" / "ipsp.db").as_posix()
    return URL.create(drivername="sqlite", database=database_path).render_as_string(
        hide_password=False
    )


class DatabaseSettings(BaseModel):
    """Validated configuration for the local SQLite control plane."""

    model_config = ConfigDict(frozen=True, extra="forbid", hide_input_in_errors=True)

    url: str = Field(default_factory=_default_database_url)
    echo: bool = False
    connection_timeout_seconds: float = Field(default=5.0, gt=0, le=60)

    @field_validator("url")
    @classmethod
    def validate_sqlite_url(cls, value: str) -> str:
        try:
            parsed = make_url(value)
        except ArgumentError:
            raise ValueError("Database URL must be a valid SQLite URL") from None
        if parsed.drivername not in {"sqlite", "sqlite+pysqlite"}:
            raise ValueError("Only synchronous SQLite database URLs are supported")
        if parsed.username is not None or parsed.password is not None or parsed.host is not None:
            raise ValueError("SQLite database URLs must not contain credentials or a host")
        return value


_COOKIE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_HEADER_NAME_PATTERN = re.compile(r"^[A-Za-z0-9-]{1,64}$")


class AuthSettings(BaseModel):
    """Non-secret authentication and browser-session policy."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    session_ttl_minutes: int = Field(default=480, gt=0, le=43_200)
    failed_login_threshold: int = Field(default=5, ge=1, le=100)
    lockout_minutes: int = Field(default=15, gt=0, le=10_080)
    session_cookie_name: str = "ipsp_session"
    csrf_cookie_name: str = "ipsp_csrf"
    csrf_header_name: str = "X-CSRF-Token"
    cookie_secure: bool = True
    cookie_samesite: Literal["lax", "strict"] = "lax"

    @field_validator("session_cookie_name", "csrf_cookie_name")
    @classmethod
    def validate_cookie_name(cls, value: str) -> str:
        if not _COOKIE_NAME_PATTERN.fullmatch(value):
            raise ValueError("Cookie names must contain only safe ASCII characters")
        return value

    @field_validator("csrf_header_name")
    @classmethod
    def validate_header_name(cls, value: str) -> str:
        if not _HEADER_NAME_PATTERN.fullmatch(value):
            raise ValueError("CSRF header name must contain only safe ASCII characters")
        return value

    @model_validator(mode="after")
    def validate_distinct_cookie_names(self) -> Self:
        if self.session_cookie_name == self.csrf_cookie_name:
            raise ValueError("Session and CSRF cookie names must be distinct")
        return self


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
        hide_input_in_errors=True,
    )

    environment: Environment = Environment.DEVELOPMENT
    app_name: str = "IPSP"
    app_version: str = "0.1.1"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    data_dir: Path = Field(default_factory=lambda: _repository_root() / "data")
    artifacts_dir: Path = Field(default_factory=lambda: _repository_root() / "artifacts")
    log_dir: Path = Field(default_factory=lambda: _repository_root() / "logs")
    frontend_dir: Path = Field(default_factory=lambda: _repository_root() / "frontend")
    default_theme: Literal["system", "dark", "light"] = "system"
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    features: FeatureFlags = Field(default_factory=FeatureFlags)
    outbound: OutboundSettings = Field(default_factory=OutboundSettings)
    secrets: SecretSettings = Field(default_factory=SecretSettings)

    @model_validator(mode="after")
    def validate_safe_environment(self) -> Self:
        """Reject unsafe process behavior without coupling features to permissions."""
        if self.environment is Environment.PRODUCTION and self.debug:
            raise ValueError("Debug mode must be disabled in production")
        if self.environment is Environment.PRODUCTION and not self.auth.cookie_secure:
            raise ValueError("Secure authentication cookies are required in production")
        return self

    def safe_snapshot(self) -> dict[str, Any]:
        """Return the complete non-secret configuration for diagnostics or hashing."""
        return self.model_dump(mode="json")
