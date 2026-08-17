# Backup, Retention & Recovery

## Status and boundary

This is a target lifecycle contract. F2-G does not implement a backup engine, storage provider,
schedule, restore workflow, migration, or readiness dependency. Backup scope expands only as owning
capabilities are implemented.

## Backup scope

The current/future backup manifest can represent, when present and policy-eligible:

- SQLite control-plane database and Alembic revision/application compatibility;
- non-secret configuration and policy metadata plus secret references, never secret values;
- project/dataset/source/table/version metadata and immutable source/processed analytical artifacts
  according to configured inclusion and retention;
- Semantic Manifests, relationships, Metric & Formula Registry, Domain Experience activation, and
  CrossDomainSemanticGraph versions;
- capabilities, Engine/Runtime Inventory/Resolver and LicenseRegistry metadata/decisions;
- model/library/artifact, base model weight, Local AI adapter, training/evaluation, promotion and
  reproducibility metadata, subject to artifact licenses;
- ScenarioIntentManifest, assumptions, CompositeSimulationGraph, results/history/artifacts, Trust,
  Evidence Profiles/snapshots, and compare/reproduction state;
- SimulationLearningStore, observed-outcome references, OutcomeReconciliation, eligibility, training-
  dataset/evaluation and promotion/rejection records, kept distinct from empirical analytical data;
- jobs/attempts, audit/governance records, report/export metadata/artifacts, and retention/deletion
  dependencies.

External evidence, provider responses, model weights, source data, and generated artifacts are
included only when policy, consent, privacy, license, location, and retention permit. Otherwise the
manifest records governed references and the resulting restoration/reproducibility limitation.

## Backup manifest and integrity

Each backup records stable ID/version, creation actor/time, application/schema versions, included and
excluded resource classes/versions, storage locations, checksums, encryption/protection metadata,
policy/retention/license snapshot, parent/incremental relation if applicable, and audit/trace.
Credentials and encryption keys remain in approved secret/key providers.

## Retention and deletion

Retention policies distinguish source/processed data, control metadata, simulations/results,
evidence/memory, learning/training/evaluation artifacts, models/adapters/weights, logs/audit, reports,
jobs, and backups. Legal/policy holds, consent withdrawal, license expiry, privacy deletion, superseded
versions, and reproducibility dependencies are handled explicitly.

Deletion is dependency-aware and audited. It never silently reclassifies evidence, leaves an orphan
presented as reproducible, or claims an adapted model has forgotten content without verified
remediation. Audit integrity may retain minimal non-sensitive decision records where authorized.

## Restore and recovery

Restore validates manifest/checksums, encryption/key availability, schema/application compatibility,
migration path, resource dependencies, artifact integrity, permissions, privacy/retention, licenses,
and safe target location before replacing active state. Restore uses staging and an atomic/rollback-
capable cutover where practical and is always audited.

Restored configuration or metadata does not automatically reactivate a disabled/unlicensed provider,
expired consent, revoked evidence source, unavailable model/adapter, blocked connector, or obsolete
learning candidate. Current security, license, provider, and policy gates are re-evaluated. Historical
references remain honest when an external artifact cannot be restored.

## Operational requirements

- Manual authorized Admin backup is the bounded v1.0 requirement; automation is optional later scope.
- Backup/restore operations use provider-neutral jobs where long-running.
- Recovery tests verify integrity, compatibility, authorization, expected exclusions, and documented
  recovery objectives once those objectives are frozen.
- Backup failure is safe and observable and does not corrupt active state or leak sensitive material.

Exact schedules, retention durations, RPO/RTO, storage backends, encryption mechanism, artifact
packaging, and restore APIs/UI are deferred to accepted owning contracts.
