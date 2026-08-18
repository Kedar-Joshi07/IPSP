# REST API Contract — Domain Map

Future resource-family ownership is governed by the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md); this map does not freeze endpoint
shapes ahead of their owning milestones.

## Status and compatibility boundary

Business, application, and Administration REST APIs preserve the `/api/v1` compatibility root.
The intentionally unversioned liveness/readiness probes remain exceptions described below.

This document identifies current and future ownership domains. It does not claim that a future
resource or route is implemented. The accepted v0.1.0 surface is limited to the verified foundation
routes documented in the [README](../README.md). v0.2.0 and later capability APIs are NOT STARTED.

F2-G does not add routes, request/response schemas, OpenAPI operations, persistence, or authorization
rules in code. Exact paths, nesting, pagination, filters, commands, idempotency, compatibility, and
authorization matrices arrive only with each owning milestone; this map avoids premature endpoint
design.

## Current API ownership

Foundation route modules remain owned under `backend/ipsp/api/routes/`. Domain packages expose typed
services and policies rather than duplicate routers or leak repository/ORM concerns. Current health,
authentication/session, jobs, and authorized Admin system behavior remains defined by accepted code,
tests, and README evidence.

## Future conceptual resource families

Future `/api/v1` contracts must have coherent ownership for:

| Resource family | Conceptual ownership; not an endpoint declaration |
|---|---|
| Projects, data, versions, and provenance | Workspace membership/policy, ingestion/artifacts, immutable dataset/table/source versions, sampling/classification/provenance, retention and lineage |
| Semantic and relationship contracts | Dataset Semantic Manifest, confirmations/conflicts, relationships/hierarchies/feature lineage, and CrossDomainSemanticGraph state |
| Metrics and Domain Experiences | Metric & Formula Registry definitions/dependencies/validation and Domain Experience manifests, compatibility, activation/limitation/refusal |
| Capability and providers | Capability decisions separate from EngineRegistry, Runtime Engine Inventory, EngineResolver, LicenseRegistry, resource/security, and provider availability |
| Models and lifecycle | Model/artifact versions, training/evaluation, baseline/challenger/champion, drift/calibration/robustness, promotion/rejection/rollback, and reproducibility |
| Scenarios, graphs, runs, and results | ScenarioIntentManifest, assumptions/constraints, CompositeSimulationGraph, execution/job state, results/uncertainty, Cross-Domain reconciliation, partial/refused paths, and lineage |
| Trust and Evidence | Separate Trust decomposition/checks and Evidence Profile/snapshot composition, limitations, provenance, and policy/license context |
| History, compare, and exports | Immutable results/artifacts, compare, re-run versus reproduce, authorized PDF/Excel or later formats, retention and audit |
| Governed learning | SimulationLearningStore references, observed-outcome matching/OutcomeReconciliation, eligibility, training-dataset/evaluation state, promotion/rejection, and corrections |
| LLM, Local AI, and evidence access | LLM/evidence modes and providers, retrieval/memory, local model/base-weight/adapter/evaluation metadata, license/policy/consent, and safe availability status |
| Jobs and operations | Provider-neutral asynchronous jobs/attempts, system configuration, policy/license administration, health, audit/log access, backups/restores, and retention |

Resource families do not determine whether a concept is nested under organization, project, dataset,
scenario, run, registry, or Administration. That choice remains with the owning freeze.

## Contract and capability status

Responses for capability/provider operations distinguish implemented, available/eligible, limited,
disabled, blocked, refused, unavailable, and planned/not-implemented states as the owning schema
defines. A frozen target, registry declaration, configured provider, installed library, feature flag,
or visible UI entry is never returned as operational capability by itself.

Async work returns stable job/run/resource identity and status links only after authorization and
accepted submission. Submission success is not execution success; workers revalidate mutable policy,
consent, license, provider, and learning gates at execution time.

## Versioning and reproducibility

Requests/results reference exact dataset/table, Semantic Manifest, metric, Domain Experience,
relationship/graph, capability, model/artifact, engine/provider/license, Scenario Intent, evidence,
policy/consent, Trust, and learning versions where relevant. Mutable labels are not sufficient for a
reproducible operation.

Contract/API schema versions are distinct from application versions and resource versions. Backward-
compatible additions remain under `/api/v1`; breaking semantics require explicit compatibility and
migration policy rather than silently changing historical payload meaning.

## Security, privacy, and error rules

- Pydantic request/response schemas; no database ORM objects leak directly.
- Authentication and role/resource/project/dataset authorization occur server-side.
- Evidence/outbound permission is Admin policy ∩ project/dataset policy ∩ runtime user consent.
- License, provider, privacy, Trust, and LearningEligibilityGate failures cannot be overridden by an
  endpoint, feature flag, or client assertion.
- Responses follow a stable error envelope with safe code/message, trace ID, optional authorized
  field details, and recoverability/clarification hints.
- Enumeration, hidden-resource, configuration, credential, policy, evidence, and raw-stack leakage is
  prohibited.
- Idempotency, optimistic concurrency/version preconditions, pagination/limits, cancellation/retry,
  and artifact authorization are frozen by owning resource contracts rather than assumed globally.

## Health routes

- `/health/live` is an intentionally unversioned infrastructure probe reporting process liveness
  without rich diagnostics.
- `/health/ready` is an intentionally unversioned probe reporting only whether required current
  database/storage/runtime dependencies can serve traffic.
- `/api/v1/admin/system/health` is the versioned application/Admin resource and may expose sanitized
  rich diagnostics only to authorized Admin users.

Optional, disabled, planned, or not-implemented engines/providers/evidence/learning/Local AI services
do not make current readiness fail. Health never invokes prohibited outbound access or leaks secrets.
