"""Honest Phase 1A readiness checks that do not claim unavailable dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from ipsp.config.settings import Settings


@dataclass(frozen=True, slots=True)
class ReadinessResult:
    """Current readiness result and explicitly deferred dependency checks."""

    ready: bool
    checks: dict[str, str]
    deferred_checks: tuple[str, ...]


class ReadinessService:
    """Evaluate only dependencies implemented in the current phase."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def check(self) -> ReadinessResult:
        return ReadinessResult(
            ready=bool(self._settings.app_name and self._settings.app_version),
            checks={"application": "ready", "configuration": "ready"},
            deferred_checks=("database", "analytical_storage", "job_worker"),
        )
