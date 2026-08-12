"""Honest readiness checks for implemented foundation dependencies."""

from __future__ import annotations

import os
from dataclasses import dataclass

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from ipsp.config.settings import Settings
from ipsp.database.migrations import MigrationStateError, MigrationStateService
from ipsp.jobs.contracts import JobBackend

DATABASE_UNAVAILABLE = "SYS-DATABASE-UNAVAILABLE"
DATABASE_FK_DISABLED = "SYS-DATABASE-FK-DISABLED"
MIGRATION_STATE_UNAVAILABLE = "SYS-MIGRATION-STATE-UNAVAILABLE"
MIGRATION_REQUIRED = "SYS-MIGRATION-REQUIRED"
STORAGE_UNAVAILABLE = "SYS-STORAGE-UNAVAILABLE"
JOB_WORKER_NOT_READY = "SYS-JOB-WORKER-NOT-READY"

DEFERRED_CHECKS = ("analytical_storage",)


@dataclass(frozen=True, slots=True)
class ReadinessResult:
    """Current readiness result and explicitly deferred dependency checks."""

    ready: bool
    checks: dict[str, str]
    deferred_checks: tuple[str, ...]
    error_code: str | None = None


class ReadinessService:
    """Separate pre-worker startup safety from complete runtime readiness."""

    def __init__(
        self,
        settings: Settings,
        engine: Engine,
        migration_state: MigrationStateService,
        job_backend: JobBackend,
    ) -> None:
        self._settings = settings
        self._engine = engine
        self._migration_state = migration_state
        self._job_backend = job_backend

    def check_startup_preconditions(self) -> ReadinessResult:
        """Check required dependencies that must be ready before worker startup."""
        checks = {
            "application": "ready",
            "configuration": "ready",
            "database": "not_checked",
            "foreign_keys": "not_checked",
            "migration": "not_checked",
            "runtime_logs": "not_checked",
            "job_worker": "not_checked",
        }
        if not self._settings.app_name or not self._settings.app_version:
            checks["application"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=DEFERRED_CHECKS,
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
                deferred_checks=DEFERRED_CHECKS,
                error_code=DATABASE_UNAVAILABLE,
            )

        checks["database"] = "ready"
        if foreign_keys_enabled != 1:
            checks["foreign_keys"] = "not_ready"
            checks["migration"] = "not_checked"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=DEFERRED_CHECKS,
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
                deferred_checks=DEFERRED_CHECKS,
                error_code=MIGRATION_STATE_UNAVAILABLE,
            )

        if not migration_state.at_head:
            checks["migration"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=DEFERRED_CHECKS,
                error_code=MIGRATION_REQUIRED,
            )

        checks["migration"] = "ready"
        try:
            log_storage_ready = (
                self._settings.log_dir.exists()
                and self._settings.log_dir.is_dir()
                and os.access(self._settings.log_dir, os.R_OK | os.W_OK)
            )
        except OSError:
            log_storage_ready = False
        if not log_storage_ready:
            checks["runtime_logs"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=DEFERRED_CHECKS,
                error_code=STORAGE_UNAVAILABLE,
            )

        checks["runtime_logs"] = "ready"
        return ReadinessResult(
            ready=True,
            checks=checks,
            deferred_checks=DEFERRED_CHECKS,
        )

    def check(self) -> ReadinessResult:
        """Check complete runtime readiness, including the active local job worker."""
        preconditions = self.check_startup_preconditions()
        if not preconditions.ready:
            return preconditions

        checks = dict(preconditions.checks)
        worker = self._job_backend.health()
        if not worker.running or not worker.accepting_jobs:
            checks["job_worker"] = "not_ready"
            return ReadinessResult(
                ready=False,
                checks=checks,
                deferred_checks=DEFERRED_CHECKS,
                error_code=JOB_WORKER_NOT_READY,
            )

        checks["job_worker"] = "ready"
        return ReadinessResult(
            ready=True,
            checks=checks,
            deferred_checks=DEFERRED_CHECKS,
        )
