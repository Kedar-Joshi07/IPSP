# SQLite Schema Specification

Post-foundation persistence ownership follows the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and its milestone contract gates.

## Status boundary

This document is a target **control-plane conceptual domain map**, not a proposed migration and not a
claim that every domain exists. The accepted v0.1.0 database contains exactly seven foundation tables:
`roles`, `permissions`, `role_permissions`, `users`, `user_sessions`, `audit_events`, and `jobs`.

F2-G adds no tables, columns, indexes, foreign keys, ORM models, repositories, or migration revisions.
Each future persistence contract and migration arrives only in its owning accepted application
milestone. Exact names, normalization, keys, indexes, retention, archival, and compatibility are
deferred to those freezes.

## Plane and ownership boundary

SQLite is the control, governance, knowledge/registry, security, and operational metadata plane.
Immutable source files and processed Parquet remain the analytical data plane. SQLite is not the
mandatory large analytical warehouse, and SimulationLearningStore experience is not silently joined
or unioned into empirical analytical data.

Repositories own data access. Application/API services do not scatter SQL or expose ORM objects.
Provider libraries, Domain Experiences, and benchmark schemas never own generic persistence.

## Accepted foundation schema

The seven implemented tables support:

- role-to-permission authorization without a persisted `is_admin` authority;
- user identity and Argon2 password hashes;
- server-side session token hashes and non-secret correlation IDs;
- durable sanitized audit/security events;
- durable local job metadata and lifecycle.

Their exact current columns and constraints are defined by the accepted Alembic history and code,
not retroactively changed by this target map.

## Future conceptual persistence homes

The following are conceptual ownership domains. They intentionally do not specify table names.

| Conceptual home | Future contract must be able to represent |
|---|---|
| Workspace, data, and provenance | Project/membership/policy; dataset/source/table/field identities; immutable dataset versions; upload/artifact, sampling, classification, retention, and provenance lineage |
| Semantic and relationships | Dataset Semantic Manifest versions; concepts/roles/grain/time/unit/currency; confirmations/conflicts; relationships, hierarchies, feature lineage, and CrossDomainSemanticGraph metadata/evidence |
| Metric & Formula Registry | Metric/definition identity and versions; typed formulas/dependencies; aggregation, grain, time, unit/currency, null/safe-division behavior; validation and lineage |
| Domain Experience activation | Pack/manifest/provider versions, compatibility, prerequisite evidence, activation/limitation/refusal, organization precedence, and UI/terminology metadata references |
| Capability, engine, and license governance | Capability decisions; EngineRegistry and Runtime Engine Inventory; EngineResolver candidates/result; LicenseRegistry dependency, model-weight, solver, dataset/evidence, connector, and provider metadata/decisions |
| Models and evaluation | Model/artifact/feature versions; libraries/providers/resources; baselines, candidates/challengers/champions; metrics, calibration, stability/drift/robustness, promotion/rejection, Trust, license, and reproducibility |
| Scenario Intent and assumptions | Versioned ScenarioIntentManifest; exact basis, objective/scope, controls, constraints, assumptions, comparison/evidence/consent snapshots, validation, and supersession |
| Composite simulation | CompositeSimulationGraph identity/version, nodes/edges/plan, CrossDomainSemanticGraph references, provider/metric/model dependencies, reconciliation, support, partial/refused paths, and result lineage |
| Trust and Evidence | Dimension/check versions/outcomes/reasons plus separate Evidence Profiles/snapshots, composition/dependence, provenance, freshness, policy/consent/license, and immutable result references |
| Simulation history/results | Run/result identity and versions; inputs/outputs/uncertainty, artifacts, compare/re-run/reproduce manifest, warnings/refusals, seeds/configuration, trace, and retention |
| Governed learning | SimulationLearningStore experience kept logically separate from empirical data; observed-outcome references/matches, OutcomeReconciliation, LearningEligibilityGate, Training Dataset Builder, evaluation and promotion/rejection decisions |
| Local AI and evidence access | LLM/evidence provider metadata; local model/base weight/adapter/evaluation versions; retrieval/memory/training snapshots; dependency/model-weight licenses; policy/consent and provenance without secret values |
| Operations | Jobs/attempts/artifacts, audit/observability references, notifications, health snapshots as appropriate, backup/restore manifests, and retention/deletion decisions |

This map gives future migrations a coherent home without requiring a one-table-per-concept design or
prejudging resource nesting.

## Versioning, lineage, and provenance rules

- Versioned contracts become immutable once referenced by a completed result, model, evidence,
  learning decision, export, or reproduction manifest; corrections create a new version.
- References use stable identities and exact versions rather than mutable labels.
- Provenance classes remain distinct. Synthetic data, assumptions, LLM proposals, prior simulations,
  external evidence, derived observations, and observed outcomes are never collapsed into one truth
  flag or empirical table.
- Evidence Profile remains separate from Trust. SimulationLearningStore remains separate from source/
  Parquet analytical data and governed training-dataset artifacts.
- Secrets are references only. Raw bearer tokens, credentials, model/license keys, and auth cookies
  are never stored in ordinary control-plane fields.
- Large payloads/artifacts remain in approved artifact/data storage with checksums and metadata
  references where appropriate.

## Security and operational rules

- Foreign keys are enabled and migration history is mandatory.
- `database/migrations/` is the single Alembic history.
- The SQLite control plane uses synchronous SQLAlchemy 2.x repositories with `select()`,
  `Session.execute()`, and `Session.scalars()`; legacy `Session.query()` and synchronous Session work
  hidden inside `async def` are prohibited.
- Authorization, project/dataset policy, privacy, consent, outbound, learning eligibility, and
  license/provider gates are service authorities; schema presence never grants permission.
- Audit metadata uses non-secret correlation and immutable resource/version references.
- Retention/deletion/backup is dependency-aware and records loss of reproducibility honestly.

## Migration ownership and sequencing

A conceptual home is not migration authorization. Metric, Domain Experience, engine/license, model,
scenario, graph, Trust/Evidence, learning/reconciliation, Local AI, evidence-provider, and operations
records are introduced only by their owning milestone's accepted functional, schema, API, acceptance,
and dependency/license contracts. F2-G creates no migration and does not reserve physical names.
