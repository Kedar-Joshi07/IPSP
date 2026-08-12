"""Typed rich system-health response contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

ComponentStatus = Literal[
    "healthy",
    "degraded",
    "unhealthy",
    "not_configured",
    "not_implemented",
    "not_available",
    "not_initialized",
    "never_run",
]


class _HealthModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReadinessHealthResponse(_HealthModel):
    ready: bool
    checks: dict[str, str]
    deferred_checks: tuple[str, ...]
    error_code: str | None


class DatabaseHealthResponse(_HealthModel):
    status: ComponentStatus
    connectivity: bool
    foreign_keys_enabled: bool | None
    migration_at_head: bool | None
    integrity_status: Literal["ok", "failed", "not_available"]
    database_size_bytes: int | None


class StorageHealthResponse(_HealthModel):
    name: Literal["data", "artifacts", "logs"]
    status: ComponentStatus
    exists: bool
    is_directory: bool
    readable: bool
    writable: bool
    free_bytes: int | None
    display_path: str
    required_now: bool


class JobWorkerHealthResponse(_HealthModel):
    status: ComponentStatus
    running: bool
    accepting_jobs: bool
    worker_count: int
    queue_depth: int
    persisted_queued_jobs: int | None


class LocalLLMHealthResponse(_HealthModel):
    feature_enabled: bool
    configured: bool
    status: ComponentStatus
    reachable: bool | None


class RemoteLLMHealthResponse(_HealthModel):
    feature_enabled: bool
    internet_enabled: bool
    remote_llm_policy_enabled: bool
    allowed_provider_count: int
    configured: bool
    status: ComponentStatus
    reachability_status: Literal["policy_disabled", "not_implemented"]


class OutboundPolicyHealthResponse(_HealthModel):
    internet_enabled: bool
    remote_llm_enabled: bool
    model_download_enabled: bool
    update_check_enabled: bool
    default_remote_transmission: str
    allowed_remote_provider_count: int


class ModelArtifactHealthResponse(_HealthModel):
    status: ComponentStatus
    storage_accessible: bool
    display_path: str


class BackupHealthResponse(_HealthModel):
    status: Literal[
        "never_run",
        "queued",
        "running",
        "succeeded",
        "failed",
        "cancelled",
        "not_available",
    ]
    job_id: str | None
    updated_at: datetime | None
    finished_at: datetime | None
    error_code: str | None


class CriticalErrorSummaryResponse(_HealthModel):
    timestamp_utc: datetime
    event_id: str
    trace_id: str | None
    component: str
    action: str
    error_code: str | None


class CriticalErrorsHealthResponse(_HealthModel):
    status: ComponentStatus
    entries: tuple[CriticalErrorSummaryResponse, ...]
    maximum_entries: int


class RuntimeHealthResponse(_HealthModel):
    logical_cpu_count: int | None
    process_memory_bytes: int | None
    load_average_1m: float | None


class SystemHealthResponse(_HealthModel):
    """Authorized rich health document without raw configuration or diagnostics."""

    status: Literal["healthy", "degraded", "unhealthy"]
    timestamp_utc: datetime
    readiness: ReadinessHealthResponse
    database: DatabaseHealthResponse
    storage: tuple[StorageHealthResponse, ...]
    job_worker: JobWorkerHealthResponse
    local_llm: LocalLLMHealthResponse
    remote_llm: RemoteLLMHealthResponse
    outbound_policy: OutboundPolicyHealthResponse
    model_artifacts: ModelArtifactHealthResponse
    backup: BackupHealthResponse
    recent_critical_errors: CriticalErrorsHealthResponse
    runtime: RuntimeHealthResponse
