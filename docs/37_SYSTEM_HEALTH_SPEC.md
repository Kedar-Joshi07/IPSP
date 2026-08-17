# System Health Specification

## Status and boundary

The accepted foundation health routes remain current. F2-G extends the **target diagnostic model**
only; unimplemented, optional, disabled, or policy-blocked F-002 services are not current readiness
requirements and do not make v0.1.1 unhealthy.

## Liveness

The unauthenticated liveness endpoint reports only that the process is alive. It performs no rich
dependency diagnostics and leaks no configuration, version inventory, provider state, or policy.

## Readiness

The readiness endpoint evaluates only dependencies required to serve the currently implemented and
enabled application safely, including applicable SQLite, migration, storage, and local runtime facts.
It returns minimal safe status and stable error code.

A planned or absent engine, evidence provider, connector, learning service, Local AI model/adapter,
Cross-Domain executor, export provider, or backup service is **not** a readiness failure unless an
accepted implementation/configuration explicitly makes it required and enabled. Optional degraded
capability is reported separately from core readiness.

## Authorized Admin diagnostics

The Admin health surface may report implemented/current categories such as:

- application/build/configuration and migration compatibility;
- SQLite connectivity/integrity, storage paths/free space, and artifact accessibility;
- LocalJobBackend/worker state, queue depth, stale attempts, and recent failures;
- authentication/session, outbound-policy state, redaction/audit sink, and recent critical errors;
- model artifact access, last backup/restore status, and bounded CPU/memory/disk summary.

As owning services become implemented, the same surface can represent:

- EngineRegistry declarations separately from Runtime Engine Inventory installed/loadable/healthy/
  enabled facts and EngineResolver availability;
- dependency, model-weight, solver, evidence, connector, and provider license gate status/expiry;
- Local/Remote LLM and synthetic/optimizer/causal/other providers without assuming candidates are
  installed;
- evidence provider/connector availability, freshness, policy eligibility, and last authorized check;
- learning/reconciliation/training builder/monitor runs and their safe state;
- local model/base-weight/adapter presence, compatibility, evaluation/promotion, resource, and
  license state;
- simulation/Composite/Cross-Domain execution availability, queue/resource state, and recent
  reconciliation failures;
- Trust/Evidence, export, backup, retention, and recovery subsystem status.

Unknown, never checked, not installed, disabled, policy-blocked, license-blocked, unavailable,
degraded, and healthy remain distinct. Target categories do not create probes or dependencies.

## Probe governance

Health checks use bounded timeouts, least privilege, approved safe methods, and cache/rate limits.
They do not download packages/models, transmit dataset content, retrieve public evidence, invoke a
billable provider, or expand evidence-access mode merely to test health. A remote/connector reachability
test runs only when that provider is implemented, configured, policy/license eligible, and explicitly
authorized for health probing.

## Security, observability, and failure

Health responses never expose secrets, credential references useful to an attacker, raw filesystem
details, sensitive data/evidence, model content, internal stack traces, or hidden resource existence.
Rich diagnostics require authorization and are audited. Public probes remain minimal.

Implementations use explicit exception handling and sanitized stable reasons; bare exception handlers
and raw diagnostics are prohibited. Probe failure reports the affected required or optional component
accurately without converting an optional failure into core outage or masking a required failure.

Exact diagnostic schemas, thresholds, refresh cadence, dashboards, alerts, and future provider probes
arrive only with their owning implementation milestones.
