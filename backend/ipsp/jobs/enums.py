"""Stable job lifecycle and generic job-family values."""

from enum import StrEnum


class JobStatus(StrEnum):
    """Persistable job lifecycle states."""

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class JobType(StrEnum):
    """Dataset-agnostic long-running operation families."""

    UPLOAD_PROCESSING = "UPLOAD_PROCESSING"
    PROFILING = "PROFILING"
    RELATIONSHIP_ANALYSIS = "RELATIONSHIP_ANALYSIS"
    MODEL_TRAINING = "MODEL_TRAINING"
    SYNTHETIC_FITTING = "SYNTHETIC_FITTING"
    SIMULATION = "SIMULATION"
    REPORT_GENERATION = "REPORT_GENERATION"
    BACKUP = "BACKUP"
    RESTORE = "RESTORE"
