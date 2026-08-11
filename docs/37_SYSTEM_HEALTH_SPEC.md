# System Health Specification

## Liveness

The unauthenticated liveness endpoint reports only that the process is alive. It performs no rich dependency diagnostics and leaks no configuration.

## Readiness

The readiness endpoint determines whether required SQLite, storage, migration, and runtime dependencies can safely serve traffic. It returns a minimal safe status and stable error code.

## Admin diagnostics

The authorized Admin health dashboard should report at minimum:
- SQLite connectivity/integrity status
- Storage paths/free disk
- Job worker health/queue depth
- Local LLM configured/health
- Remote LLM configured/reachable if policy allows test
- Outbound internet policy state
- Model artifact access
- Last backup status
- Recent critical errors
- Memory/CPU summary where feasible

Health checks must not leak secrets or sensitive data.
Health implementations use explicit exception handling and sanitized responses; bare exception handlers and raw diagnostics are prohibited.
