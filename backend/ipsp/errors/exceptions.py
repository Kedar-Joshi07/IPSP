"""Domain-safe exceptions independent of FastAPI and HTTP concerns."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from ipsp.security.redaction import JsonSafeValue, sanitize_details

_ERROR_CODE_PATTERN = re.compile(
    r"^(AUTH|AUTHZ|DATA|SEM|REL|ML|LLM|SIM|TRUST|EXP|JOB|SYS)-[A-Z0-9_]+$"
)


class IPSPError(Exception):
    """Base exception carrying a stable code and client-safe message."""

    def __init__(
        self,
        error_code: str,
        safe_message: str,
        *,
        recoverable: bool = False,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        if not _ERROR_CODE_PATTERN.fullmatch(error_code):
            raise ValueError(f"Invalid IPSP error code: {error_code}")
        super().__init__(safe_message)
        self.error_code = error_code
        self.safe_message = safe_message
        self.recoverable = recoverable
        self.details: dict[str, JsonSafeValue] | None = sanitize_details(details)
