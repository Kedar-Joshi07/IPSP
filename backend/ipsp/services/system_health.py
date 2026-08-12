"""Sanitized rich system diagnostics for explicitly authorized callers."""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from uuid import UUID

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from ipsp.config.settings import Settings
from ipsp.database.migrations import MigrationStateError, MigrationStateService
from ipsp.database.session import DatabaseSessionFactory
from ipsp.jobs.contracts import JobBackend
from ipsp.jobs.enums import JobStatus, JobType
from ipsp.observability.logging import DEFAULT_BACKUP_COUNT, RUNTIME_LOG_NAME
from ipsp.repositories.jobs import JobRepository
from ipsp.security.outbound import OutboundPolicy
from ipsp.services.readiness import ReadinessService

MAX_CRITICAL_ERRORS = 10
MAX_LOG_BYTES_PER_FILE = 256 * 1024
_SAFE_CONTEXT_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
_SAFE_EVENT_TEXT = re.compile(r"^[a-z][a-z0-9._-]{0,127}$")
_SAFE_ERROR_CODE = re.compile(r"^[A-Z]{2,10}-[A-Z0-9_-]{1,117}$")


class HealthState(StrEnum):
    """Bounded health vocabulary shared by rich diagnostic components."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    NOT_CONFIGURED = "not_configured"
    NOT_IMPLEMENTED = "not_implemented"
    NOT_AVAILABLE = "not_available"
    NOT_INITIALIZED = "not_initialized"
    NEVER_RUN = "never_run"


@dataclass(frozen=True, slots=True)
class ReadinessDiagnostics:
    ready: bool
    checks: dict[str, str]
    deferred_checks: tuple[str, ...]
    error_code: str | None


@dataclass(frozen=True, slots=True)
class DatabaseDiagnostics:
    status: HealthState
    connectivity: bool
    foreign_keys_enabled: bool | None
    migration_at_head: bool | None
    integrity_status: str
    database_size_bytes: int | None


@dataclass(frozen=True, slots=True)
class StorageDiagnostics:
    name: str
    status: HealthState
    exists: bool
    is_directory: bool
    readable: bool
    writable: bool
    free_bytes: int | None
    display_path: str
    required_now: bool


@dataclass(frozen=True, slots=True)
class JobWorkerDiagnostics:
    status: HealthState
    running: bool
    accepting_jobs: bool
    worker_count: int
    queue_depth: int
    persisted_queued_jobs: int | None


@dataclass(frozen=True, slots=True)
class LocalLLMDiagnostics:
    feature_enabled: bool
    configured: bool
    status: HealthState
    reachable: bool | None


@dataclass(frozen=True, slots=True)
class RemoteLLMDiagnostics:
    feature_enabled: bool
    internet_enabled: bool
    remote_llm_policy_enabled: bool
    allowed_provider_count: int
    configured: bool
    status: HealthState
    reachability_status: str


@dataclass(frozen=True, slots=True)
class OutboundPolicyDiagnostics:
    internet_enabled: bool
    remote_llm_enabled: bool
    model_download_enabled: bool
    update_check_enabled: bool
    default_remote_transmission: str
    allowed_remote_provider_count: int


@dataclass(frozen=True, slots=True)
class ModelArtifactDiagnostics:
    status: HealthState
    storage_accessible: bool
    display_path: str


@dataclass(frozen=True, slots=True)
class BackupDiagnostics:
    status: str
    job_id: str | None
    updated_at: datetime | None
    finished_at: datetime | None
    error_code: str | None


@dataclass(frozen=True, slots=True)
class CriticalErrorSummary:
    timestamp_utc: datetime
    event_id: str
    trace_id: str | None
    component: str
    action: str
    error_code: str | None


@dataclass(frozen=True, slots=True)
class CriticalErrorDiagnostics:
    status: HealthState
    entries: tuple[CriticalErrorSummary, ...]
    maximum_entries: int


@dataclass(frozen=True, slots=True)
class RuntimeDiagnostics:
    logical_cpu_count: int | None
    process_memory_bytes: int | None
    load_average_1m: float | None


@dataclass(frozen=True, slots=True)
class SystemHealthSnapshot:
    status: HealthState
    timestamp_utc: datetime
    readiness: ReadinessDiagnostics
    database: DatabaseDiagnostics
    storage: tuple[StorageDiagnostics, ...]
    job_worker: JobWorkerDiagnostics
    local_llm: LocalLLMDiagnostics
    remote_llm: RemoteLLMDiagnostics
    outbound_policy: OutboundPolicyDiagnostics
    model_artifacts: ModelArtifactDiagnostics
    backup: BackupDiagnostics
    recent_critical_errors: CriticalErrorDiagnostics
    runtime: RuntimeDiagnostics


class SystemHealthService:
    """Collect read-only diagnostics without exposing raw configuration or failures."""

    def __init__(
        self,
        settings: Settings,
        engine: Engine,
        sessions: DatabaseSessionFactory,
        migration_state: MigrationStateService,
        readiness: ReadinessService,
        job_backend: JobBackend,
        outbound_policy: OutboundPolicy,
    ) -> None:
        self._settings = settings
        self._engine = engine
        self._sessions = sessions
        self._migration_state = migration_state
        self._readiness = readiness
        self._job_backend = job_backend
        self._outbound_policy = outbound_policy

    def check(self) -> SystemHealthSnapshot:
        """Return a typed snapshot of implemented and explicitly deferred capabilities."""
        readiness_result = self._readiness.check()
        database = self._database_diagnostics()
        storage = (
            self._storage_diagnostics("data", self._settings.data_dir, required_now=False),
            self._storage_diagnostics(
                "artifacts", self._settings.artifacts_dir, required_now=False
            ),
            self._storage_diagnostics("logs", self._settings.log_dir, required_now=True),
        )
        worker = self._job_worker_diagnostics()
        critical_errors = self._critical_error_diagnostics()
        required_states = (database.status, storage[2].status, worker.status)
        if not readiness_result.ready or HealthState.UNHEALTHY in required_states:
            overall = HealthState.UNHEALTHY
        elif critical_errors.status is HealthState.NOT_AVAILABLE:
            overall = HealthState.DEGRADED
        else:
            overall = HealthState.HEALTHY
        artifacts = storage[1]
        return SystemHealthSnapshot(
            status=overall,
            timestamp_utc=datetime.now(UTC),
            readiness=ReadinessDiagnostics(
                ready=readiness_result.ready,
                checks=dict(readiness_result.checks),
                deferred_checks=readiness_result.deferred_checks,
                error_code=readiness_result.error_code,
            ),
            database=database,
            storage=storage,
            job_worker=worker,
            local_llm=LocalLLMDiagnostics(
                feature_enabled=self._settings.features.local_llm_enabled,
                configured=False,
                status=HealthState.NOT_IMPLEMENTED,
                reachable=None,
            ),
            remote_llm=self._remote_llm_diagnostics(),
            outbound_policy=self._outbound_policy_diagnostics(),
            model_artifacts=ModelArtifactDiagnostics(
                status=artifacts.status,
                storage_accessible=artifacts.status is HealthState.HEALTHY,
                display_path=artifacts.display_path,
            ),
            backup=self._backup_diagnostics(),
            recent_critical_errors=critical_errors,
            runtime=self._runtime_diagnostics(),
        )

    def _database_diagnostics(self) -> DatabaseDiagnostics:
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                foreign_keys = connection.scalar(text("PRAGMA foreign_keys"))
                quick_check = connection.scalar(text("PRAGMA quick_check"))
                page_count = connection.scalar(text("PRAGMA page_count"))
                page_size = connection.scalar(text("PRAGMA page_size"))
        except SQLAlchemyError:
            return DatabaseDiagnostics(
                status=HealthState.UNHEALTHY,
                connectivity=False,
                foreign_keys_enabled=None,
                migration_at_head=None,
                integrity_status="not_available",
                database_size_bytes=None,
            )

        integrity_status = (
            "ok" if isinstance(quick_check, str) and quick_check.casefold() == "ok" else "failed"
        )
        size = (
            page_count * page_size
            if isinstance(page_count, int)
            and not isinstance(page_count, bool)
            and isinstance(page_size, int)
            and not isinstance(page_size, bool)
            and page_count >= 0
            and page_size >= 0
            else None
        )
        try:
            migration_at_head = self._migration_state.inspect().at_head
        except (MigrationStateError, SQLAlchemyError):
            migration_at_head = None
        healthy = foreign_keys == 1 and migration_at_head is True and integrity_status == "ok"
        return DatabaseDiagnostics(
            status=HealthState.HEALTHY if healthy else HealthState.UNHEALTHY,
            connectivity=True,
            foreign_keys_enabled=foreign_keys == 1,
            migration_at_head=migration_at_head,
            integrity_status=integrity_status,
            database_size_bytes=size,
        )

    @staticmethod
    def _storage_diagnostics(
        name: str,
        path: Path,
        *,
        required_now: bool,
    ) -> StorageDiagnostics:
        display_path = path.name or "<configured>"
        try:
            exists = path.exists()
            is_directory = path.is_dir()
            readable = is_directory and os.access(path, os.R_OK)
            writable = is_directory and os.access(path, os.W_OK)
            free_bytes = shutil.disk_usage(path).free if is_directory else None
        except OSError:
            return StorageDiagnostics(
                name=name,
                status=HealthState.UNHEALTHY if required_now else HealthState.NOT_AVAILABLE,
                exists=False,
                is_directory=False,
                readable=False,
                writable=False,
                free_bytes=None,
                display_path=display_path,
                required_now=required_now,
            )
        if not exists:
            state = HealthState.UNHEALTHY if required_now else HealthState.NOT_INITIALIZED
        elif not is_directory or not readable or not writable or free_bytes is None:
            state = HealthState.UNHEALTHY if required_now else HealthState.NOT_AVAILABLE
        else:
            state = HealthState.HEALTHY
        return StorageDiagnostics(
            name=name,
            status=state,
            exists=exists,
            is_directory=is_directory,
            readable=readable,
            writable=writable,
            free_bytes=free_bytes,
            display_path=display_path,
            required_now=required_now,
        )

    def _job_worker_diagnostics(self) -> JobWorkerDiagnostics:
        worker = self._job_backend.health()
        try:
            with self._sessions.session() as session:
                persisted_queued = JobRepository(session).count_by_status(JobStatus.QUEUED)
        except SQLAlchemyError:
            persisted_queued = None
        ready = worker.running and worker.accepting_jobs
        return JobWorkerDiagnostics(
            status=HealthState.HEALTHY if ready else HealthState.UNHEALTHY,
            running=worker.running,
            accepting_jobs=worker.accepting_jobs,
            worker_count=worker.worker_count,
            queue_depth=worker.queue_depth,
            persisted_queued_jobs=persisted_queued,
        )

    def _remote_llm_diagnostics(self) -> RemoteLLMDiagnostics:
        policy = self._outbound_policy.diagnostics()
        feature_enabled = self._settings.features.remote_llm_enabled
        internet_enabled = policy.internet_enabled
        policy_enabled = policy.remote_llm_enabled
        reachability = (
            "not_implemented"
            if feature_enabled and internet_enabled and policy_enabled
            else "policy_disabled"
        )
        return RemoteLLMDiagnostics(
            feature_enabled=feature_enabled,
            internet_enabled=internet_enabled,
            remote_llm_policy_enabled=policy_enabled,
            allowed_provider_count=policy.allowed_remote_provider_count,
            configured=False,
            status=HealthState.NOT_IMPLEMENTED,
            reachability_status=reachability,
        )

    def _outbound_policy_diagnostics(self) -> OutboundPolicyDiagnostics:
        outbound = self._outbound_policy.diagnostics()
        return OutboundPolicyDiagnostics(
            internet_enabled=outbound.internet_enabled,
            remote_llm_enabled=outbound.remote_llm_enabled,
            model_download_enabled=outbound.model_download_enabled,
            update_check_enabled=outbound.update_check_enabled,
            default_remote_transmission=outbound.default_transmission_level.value,
            allowed_remote_provider_count=outbound.allowed_remote_provider_count,
        )

    def _backup_diagnostics(self) -> BackupDiagnostics:
        try:
            with self._sessions.session() as session:
                record = JobRepository(session).get_latest_by_type(JobType.BACKUP)
        except SQLAlchemyError:
            return BackupDiagnostics("not_available", None, None, None, None)
        if record is None:
            return BackupDiagnostics(HealthState.NEVER_RUN.value, None, None, None, None)
        return BackupDiagnostics(
            status=record.status.casefold(),
            job_id=record.job_id,
            updated_at=record.updated_at,
            finished_at=record.finished_at,
            error_code=record.error_code,
        )

    def _critical_error_diagnostics(self) -> CriticalErrorDiagnostics:
        candidates = [self._settings.log_dir / RUNTIME_LOG_NAME]
        candidates.extend(
            self._settings.log_dir / f"{RUNTIME_LOG_NAME}.{index}"
            for index in range(1, DEFAULT_BACKUP_COUNT + 1)
        )
        found_file = False
        entries: list[CriticalErrorSummary] = []
        for path in candidates:
            try:
                lines = _bounded_tail_lines(path)
            except FileNotFoundError:
                continue
            except OSError:
                continue
            found_file = True
            for line in reversed(lines):
                summary = _decode_critical_summary(line)
                if summary is not None:
                    entries.append(summary)
                    if len(entries) == MAX_CRITICAL_ERRORS:
                        return CriticalErrorDiagnostics(
                            HealthState.HEALTHY,
                            tuple(entries),
                            MAX_CRITICAL_ERRORS,
                        )
        return CriticalErrorDiagnostics(
            HealthState.HEALTHY if found_file else HealthState.NOT_AVAILABLE,
            tuple(entries),
            MAX_CRITICAL_ERRORS,
        )

    @staticmethod
    def _runtime_diagnostics() -> RuntimeDiagnostics:
        cpu_count = os.cpu_count()
        logical_cpu_count = cpu_count if cpu_count is not None and cpu_count > 0 else None
        load_average: float | None = None
        if hasattr(os, "getloadavg"):
            try:
                load_average = os.getloadavg()[0]
            except OSError:
                load_average = None
        return RuntimeDiagnostics(
            logical_cpu_count=logical_cpu_count,
            process_memory_bytes=None,
            load_average_1m=load_average,
        )


def _bounded_tail_lines(path: Path) -> list[str]:
    with path.open("rb") as stream:
        stream.seek(0, os.SEEK_END)
        size = stream.tell()
        offset = max(0, size - MAX_LOG_BYTES_PER_FILE)
        stream.seek(offset)
        payload = stream.read(MAX_LOG_BYTES_PER_FILE)
    lines = payload.decode("utf-8", errors="replace").splitlines()
    return lines[1:] if offset and lines else lines


def _decode_critical_summary(line: str) -> CriticalErrorSummary | None:
    try:
        payload = json.loads(line)
    except (json.JSONDecodeError, RecursionError):
        return None
    if not isinstance(payload, dict) or payload.get("severity") != "CRITICAL":
        return None
    timestamp = _safe_timestamp(payload.get("timestamp_utc"))
    event_id = _safe_uuid(payload.get("event_id"))
    component = _safe_event_text(payload.get("component"))
    action = _safe_event_text(payload.get("action"))
    if timestamp is None or event_id is None or component is None or action is None:
        return None
    return CriticalErrorSummary(
        timestamp_utc=timestamp,
        event_id=event_id,
        trace_id=_safe_context_id(payload.get("trace_id")),
        component=component,
        action=action,
        error_code=_safe_error_code(payload.get("error_code")),
    )


def _safe_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or len(value) > 64:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except (OverflowError, ValueError):
        return None
    return parsed.astimezone(UTC) if parsed.tzinfo is not None else None


def _safe_uuid(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    try:
        return str(UUID(value))
    except ValueError:
        return None


def _safe_context_id(value: object) -> str | None:
    return value if isinstance(value, str) and _SAFE_CONTEXT_ID.fullmatch(value) else None


def _safe_event_text(value: object) -> str | None:
    return value if isinstance(value, str) and _SAFE_EVENT_TEXT.fullmatch(value) else None


def _safe_error_code(value: object) -> str | None:
    return value if isinstance(value, str) and _SAFE_ERROR_CODE.fullmatch(value) else None
