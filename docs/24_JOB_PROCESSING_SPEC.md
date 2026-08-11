# Background Job Processing Specification

## Long-running job types
Upload processing, profiling, relationship analysis, model training, SDV fitting, large simulation, report generation, backup/restore.

## v1 implementation
Local worker + SQLite-backed job metadata is acceptable. Keep a `JobBackend` abstraction for future RQ/Celery/Redis/distributed workers.

The v0.1.0 foundation defines `JobBackend`, `JobService`, `JobRepository`, `JobStatus`, and `JobType`, plus progress, cancellation, retry, and sanitized error contracts and the supporting job schema. Full worker execution may arrive later. Redis and Celery are not foundation requirements.

## Job states
`QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`.

## Requirements
Progress %, phase/message, timestamps, trace ID, owner, artifact references, retryability, cancellation where safe, sanitized error details.
