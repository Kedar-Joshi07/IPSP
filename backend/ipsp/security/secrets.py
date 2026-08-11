"""Secret references, protected values, and environment-backed resolution."""

from __future__ import annotations

import hmac
import os
import re
from collections.abc import Mapping
from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel, ConfigDict, field_validator

from ipsp.errors.exceptions import IPSPError

_PROVIDER_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_SECRET_KEY_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}$")


class SecretProviderKind(StrEnum):
    """Secret provider implementations selected by frozen configuration."""

    ENVIRONMENT = "environment"


def validate_provider_identifier(value: str) -> str:
    """Validate a canonical, non-secret provider identifier."""
    if not _PROVIDER_ID_PATTERN.fullmatch(value):
        raise ValueError("Provider identifiers must use lowercase letters, digits, '.', '_' or '-'")
    return value


class SecretRef(BaseModel):
    """Validated metadata reference to a secret stored outside normal configuration."""

    model_config = ConfigDict(frozen=True, extra="forbid", str_strip_whitespace=True)

    provider: str
    key: str

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        return validate_provider_identifier(value)

    @field_validator("key")
    @classmethod
    def validate_key(cls, value: str) -> str:
        if not _SECRET_KEY_PATTERN.fullmatch(value):
            raise ValueError("Secret reference keys contain unsupported characters")
        return value


class SecretValue:
    """In-process secret wrapper requiring an explicit reveal operation."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError("Secret values must not be empty")
        self._value = value

    def reveal(self) -> str:
        """Explicitly return plaintext for the narrowly scoped consumer that needs it."""
        return self._value

    def __repr__(self) -> str:
        return "SecretValue([REDACTED])"

    def __str__(self) -> str:
        return "[REDACTED]"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SecretValue) and hmac.compare_digest(
            self._value.encode("utf-8"),
            other._value.encode("utf-8"),
        )


class SecretProvider(Protocol):
    """Resolution boundary for external secret stores."""

    @property
    def provider_id(self) -> str: ...

    def get(self, ref: SecretRef) -> SecretValue | None: ...

    def require(self, ref: SecretRef) -> SecretValue: ...


class EnvironmentSecretProvider:
    """Resolve only explicitly requested values from the process environment."""

    provider_id = SecretProviderKind.ENVIRONMENT.value

    def __init__(self, environ: Mapping[str, str] | None = None) -> None:
        self._environ = os.environ if environ is None else environ

    def _validate_provider(self, ref: SecretRef) -> None:
        if ref.provider != self.provider_id:
            raise IPSPError(
                "SYS-SECRET_PROVIDER",
                "The requested secret provider is not configured.",
                details={"provider": ref.provider, "secret_ref": ref.key},
            )

    def get(self, ref: SecretRef) -> SecretValue | None:
        """Return a wrapped value or None without inspecting unrelated environment entries."""
        self._validate_provider(ref)
        value = self._environ.get(ref.key)
        return SecretValue(value) if value else None

    def require(self, ref: SecretRef) -> SecretValue:
        """Resolve a required secret or fail closed with a safe domain error."""
        value = self.get(ref)
        if value is None:
            raise IPSPError(
                "SYS-SECRET_REQUIRED",
                "A required secret is unavailable.",
                details={"provider": ref.provider, "secret_ref": ref.key},
            )
        return value
