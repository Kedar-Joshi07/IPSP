# SQLite Schema Specification

## Status boundary

This document is a target control-plane domain map, not a claim that all listed tables exist. The
accepted v0.1.0 database contains only its seven foundation tables. F-002 analytical, registry,
scenario, evidence, and learning persistence remains planned. Exact table names, columns,
normalization, keys, indexes, retention, and migrations are deferred to F2-G and the owning
milestone contract freezes.

## Major table groups

### Security
users, roles, permissions, role_permissions, user_sessions, user_preferences. V1.0 `users.role_id` resolves the user's single role; role-to-permission mapping is the only authorization authority. `users` contains `id`, unique `username`, `display_name`, nullable `email`, `password_hash`, `role_id`, `is_active`, `must_change_password`, `failed_login_count`, `locked_until`, `last_login_at`, `password_changed_at`, `created_at`, `created_by`, and `updated_at`; it has no persisted `is_admin`.

`user_sessions` stores a token hash, non-secret correlation ID, user reference, created/last-seen/expiry/invalidation timestamps, and lifecycle metadata. Raw bearer tokens are never stored or logged. Security timestamps use timezone-aware UTC semantics.

### Workspace/data
projects, project_memberships, datasets, dataset_versions, dataset_tables, dataset_columns, dataset_permissions, column_policies, upload_artifacts.

`datasets` represents logical identity; `dataset_versions` contains immutable versions. Multi-table status is derived from related `dataset_tables`, never from a persisted `is_multi_table` flag.

### Semantics
semantic_manifests, column_semantics, relationships, hierarchies, feature_lineage, semantic_conflicts, clarification_questions, user_confirmations, kpi_definitions, business_rules.

Under F-002, future semantic persistence must also support versioned Metric & Formula Registry
definitions, Domain Experience Manifests and activation, and CrossDomainSemanticGraph evidence.
`kpi_definitions` is predecessor vocabulary, not the complete registry architecture.

### Capabilities/models
capabilities, capability_validations, models, model_metrics, model_promotions, drift_metrics.

Future registry persistence must represent EngineRegistry, LicenseRegistry, and EngineResolver
decisions without making a provider library the schema owner.

### Simulation
simulation_runs, simulation_inputs, simulation_outputs, simulation_artifacts, run_warnings, trust_scores.

Future simulation persistence must preserve ScenarioIntentManifest and CompositeSimulationGraph
versions and keep Trust records distinct from Evidence Profiles.

### Governed learning

Future persistence must keep SimulationLearningStore experience logically separate from empirical
analytical data and represent observed outcomes, OutcomeReconciliation, learning eligibility, and
promotion/rejection decisions with provenance.

### AI/configuration
llm_providers, llm_usage, outbound_policies, feature_flags, system_settings, secret_references.

Future configuration metadata must represent evidence-access policy and consent snapshots while
preserving SecretProvider references and deny-by-default outbound enforcement.

### Operations
jobs, audit_events, notifications, backups.

The foundation `jobs` schema supports `JobRepository` and records job type/status, progress, owner, trace ID, timestamps, retryability, cancellation, artifact references, and sanitized error details. Audit events use `session_correlation_id`, not a bearer session identifier.

## Rules
- Versioned objects are immutable once referenced by a completed run; create a new version instead of overwriting history.
- Semantic manifests, capabilities, and model versions/artifacts are immutable once referenced. Simulation runs use exact foreign-key references to dataset, semantic, capability, and model version records and persist seeds plus an effective non-secret configuration snapshot/hash.
- Foreign keys enabled.
- Repositories own data access.
- Migration history is mandatory.
- `database/migrations/` is the single Alembic history.
- The SQLite control plane uses synchronous SQLAlchemy 2.x repositories with `select()`/`Session.execute()`/`Session.scalars()`; legacy `Session.query()` and synchronous Session work hidden inside `async def` are prohibited.
- Synthetic data, assumptions, LLM proposals, simulations, and observed outcomes retain distinct
  provenance and cannot be silently collapsed into one empirical-data authority.
