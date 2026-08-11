"""Honest readiness checks for implemented foundation dependencies."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from ipsp.config.settings import Settings
from ipsp.database.migrations import MigrationStateError, MigrationStateService

DATABASE_UNAVAILABLE = "SYS-DATABASE-UNAVAILABLE"
DATABASE_FK_DISABLED = "SYS-DATABASE-FK-DISABLED"
MIGRATION_STATE_UNAVAILABLE = "SYS-MIGRATION-STATE-UNAVAILABLE"
MIGRATION_REQUIRED = "SYS-MIGRATION-REQUIRED"


@dataclass(frozen=True, slots=True)
class ReadinessResult:
    """Current readiness result and explicitly deferred dependency checks."""

    ready: bool
    checks: dict[str, str]
    deferred_checks: tuple[str, ...]
    error_code: str | None = None


class ReadinessService:
    """Evaluate only dependencies implemented in the current phase."""

    def __init__(
        self,
        settings: Settings,
        engine: Engine,
        migration_state: MigrationStateService,
    ) -> None:
        self._settings = settings
        self._engine = engine
        self._migration_state = migration_state

    def check(self) -> ReadinessResult:
        checks = {
            "application": "ready",
            "configuration": "ready",
        }
        if not self._settings.app_name or not self._settings.app_version:
            checks["application"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=("analytical_storage", "job_worker"),
                error_code="SYS-APPLICATION-NOT-READY",
            )

        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                foreign_keys_enabled = connection.scalar(text("PRAGMA foreign_keys"))
        except SQLAlchemyError:
            checks["database"] = "not_ready"
            checks["migration"] = "not_checked"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=("analytical_storage", "job_worker"),
                error_code=DATABASE_UNAVAILABLE,
            )

        checks["database"] = "ready"
        if foreign_keys_enabled != 1:
            checks["foreign_keys"] = "not_ready"
            checks["migration"] = "not_checked"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=("analytical_storage", "job_worker"),
                error_code=DATABASE_FK_DISABLED,
            )

        checks["foreign_keys"] = "ready"
        try:
            migration_state = self._migration_state.inspect()
        except (MigrationStateError, SQLAlchemyError):
            checks["migration"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=("analytical_storage", "job_worker"),
                error_code=MIGRATION_STATE_UNAVAILABLE,
            )

        if not migration_state.at_head:
            checks["migration"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=("analytical_storage", "job_worker"),
                error_code=MIGRATION_REQUIRED,
            )

        checks["migration"] = "ready"
        return ReadinessResult(
            ready=True,
            checks=checks,
            deferred_checks=("analytical_storage", "job_worker"),
        )
