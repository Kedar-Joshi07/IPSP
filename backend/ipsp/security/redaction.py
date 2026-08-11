"""Deterministic sanitization for structured client and observability data."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import TypeAlias

REDACTED_VALUE = "[REDACTED]"
UNSUPPORTED_VALUE = "[UNSUPPORTED]"

JsonSafeValue: TypeAlias = (
    str | int | float | bool | None | list["JsonSafeValue"] | dict[str, "JsonSafeValue"]
)

_SENSITIVE_EXACT_KEYS = frozenset(
    {
        "api_key",
        "authorization",
        "client_secret",
        "cookie",
        "credential_key",
        "encryption_key",
        "password",
        "password_hash",
        "passwd",
        "private_key",
        "proxy_authorization",
        "pwd",
        "refresh_token",
        "secret",
        "secret_key",
        "session_token",
        "set_cookie",
        "signing_key",
        "token",
        "x_api_key",
    }
)
_SENSITIVE_SUFFIXES = (
    "_api_key",
    "_cookie",
    "_credential_key",
    "_encryption_key",
    "_password",
    "_password_hash",
    "_passwd",
    "_private_key",
    "_pwd",
    "_secret",
    "_secret_key",
    "_signing_key",
    "_token",
)


def _normalize_key(key: str) -> str:
    return re.sub(r"[-\s]+", "_", key.strip().casefold())


def is_sensitive_key(key: str) -> bool:
    """Return whether a structured key is explicitly credential-bearing."""
    normalized = _normalize_key(key)
    return normalized in _SENSITIVE_EXACT_KEYS or normalized.endswith(_SENSITIVE_SUFFIXES)


def sanitize_structured_data(value: object) -> JsonSafeValue:
    """Recursively redact secrets and retain only predictable JSON-safe values."""
    if isinstance(value, Mapping):
        sanitized: dict[str, JsonSafeValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                continue
            sanitized[key] = (
                REDACTED_VALUE if is_sensitive_key(key) else sanitize_structured_data(item)
            )
        return sanitized
    if isinstance(value, (list, tuple)):
        return [sanitize_structured_data(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return UNSUPPORTED_VALUE


def sanitize_details(
    details: Mapping[str, object] | None,
) -> dict[str, JsonSafeValue] | None:
    """Build the client-safe mapping accepted by the stable error envelope."""
    if details is None:
        return None
    sanitized = sanitize_structured_data(details)
    return sanitized if isinstance(sanitized, dict) else {}
