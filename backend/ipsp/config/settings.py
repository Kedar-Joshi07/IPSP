"""Phase 1A application settings and environment validation."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Supported application environments."""

    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Minimal, secret-free settings required to boot the Phase 1A foundation."""

    model_config = SettingsConfigDict(
        env_prefix="IPSP_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
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
    internet_enabled: bool = False
    remote_llm_enabled: bool = False
    default_theme: Literal["system", "dark", "light"] = "system"

    @model_validator(mode="after")
    def validate_safe_environment(self) -> Self:
        """Reject unsafe production debug and outbound-policy combinations."""
        if self.environment is Environment.PRODUCTION and self.debug:
            raise ValueError("Debug mode must be disabled in production")
        if self.remote_llm_enabled and not self.internet_enabled:
            raise ValueError("Remote LLM access requires the outbound internet policy")
        return self
