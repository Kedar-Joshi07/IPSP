# Observability & Audit Specification

## Status and boundary

The accepted v0.1.0 structured logging, trace, and durable audit foundation remains current. F-002
references below are target context fields/streams and do not imply that engines, evidence providers,
learning, Local AI, or Cross-Domain runtime exists in v0.1.1.

## Event envelope

Every event requires `timestamp_utc`, `event_id`, `trace_id`, `request_id`, `component`, `action`,
`status`, `severity`, and sanitized metadata. Include `session_correlation_id`, `user_id`, resolved
role, `duration_ms`, `error_code`, `resource_type`, `resource_id`, and relevant immutable versioned
references when the event context supplies them.

Future contextual references may cover project/dataset/table/source, semantic/metric/Domain
Experience/CrossDomainSemanticGraph, capability/model/artifact, engine/provider/inventory/resolver,
dependency/model-weight/evidence license decision, ScenarioIntent/CompositeSimulationGraph,
Trust/Evidence Profile, evidence provider/snapshot, learning/reconciliation/training/evaluation,
Local AI model/adapter, job/run/result/export, policy/consent, and backup/recovery state.

Fields are sparse and typed by event schema; events do not invent placeholder IDs for unavailable
services. `session_correlation_id` is non-secret and pseudonymous, never a raw bearer token or cookie.

## Logical streams

Audit, Security, Application, Frontend, Data Processing, Semantics/Registry, ML/Engine, LLM/Evidence,
Simulation/Cross-Domain, Trust, Learning/Reconciliation, Jobs, Performance, Export, Backup/Recovery,
Errors, and System Health.

Durable audit/security/governance decisions may be stored in SQLite. High-volume application,
frontend, processing, provider, performance, and runtime logs go to structured rotating files or
another configured sink; SQLite is not the complete runtime log warehouse.

## Required future audit decisions

When the owning capability is implemented, audit captures:

- engine/provider inventory verification, selection/exclusion/fallback, and resource/security state;
- license review/gate outcomes, subjects/versions, intended use, conditions, expiry, and reviewer;
- evidence-access and connector/provider allow/deny, consent/policy snapshots, minimization, and
  external destination without copying sensitive payloads;
- scenario/Composite/Cross-Domain validation, execution, partial/refused paths, and reconciliations;
- observed-outcome match, LearningEligibilityGate, training-dataset build, challenger evaluation,
  promotion/rejection/rollback, and drift/monitor decisions;
- Local AI retrieval/memory, model/adapter evaluation and promotion, with provenance/privacy/license;
- configuration/security/permission changes, job lifecycle, artifacts, export, deletion, backup, and
  restore decisions.

## Trace propagation

Browser action → FastAPI → authentication/RBAC/resource policy/consent → application service → job →
dataset/semantic/metric/capability → engine/provider/model/LLM/evidence → simulation/Trust/learning →
result/export, all linked by trace ID where the path applies.

Asynchronous submission records parent/causation identifiers and carries the trace context into the
worker. Retries create distinct attempt/event IDs without losing the originating trace and job/run.

## Do not log

Passwords, password hashes, API/license keys, raw cookies/tokens/auth headers, secret material,
unrestricted sensitive records, complete sensitive prompts or evidence payloads, model weight
contents, raw connector responses, or unredacted exception values. Checksums, governed references,
classifications, counts, policy decisions, and safe reason codes are preferred.

## Frontend and health telemetry

Log meaningful transitions, submissions, API/job failures, session expiry, policy/refusal, export,
and error events, filtered and rate-limited. Do not log every UI interaction.

Health observations distinguish required current dependencies from optional/planned providers. A
planned or disabled service cannot make current readiness fail. Diagnostics and audit access require
authorization and never leak secrets, sensitive data, private evidence, or raw stack traces.

## Retention, integrity, and failure

Audit retention follows legal/policy needs and preserves decision integrity, ordering, actor, and
version references. Operational logs use bounded rotation/retention. Observability failure is
reported safely; security-critical audit persistence fails closed where the owning operation requires
durable audit. Exact future schemas/sinks arrive with their owning milestones.
