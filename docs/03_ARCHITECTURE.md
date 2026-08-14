# System Architecture

## Status and authority

This is the F-002 target architecture. It extends the accepted v0.1.0 foundation; it does not claim
that post-foundation analytical layers are currently implemented. The authoritative decisions are
in the [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md).

## Target layered architecture

```text
Frontend
  → API / Authentication / RBAC / Policy / Consent
  → Ingestion / Storage
  → Data Understanding
  → Semantic + Metric Layer
  → Domain Experience Activation
  → Cross-Domain Composition
  → Capability Discovery
  → Scenario / Evidence
  → Engine / License Resolver
  → Composite Simulation Graph
  → Trust + Evidence Profile
  → Results / History / Export
  → Learning / Reconciliation
```

The layers are logical responsibility boundaries rather than permission to create a monolith or to
bypass repositories, policies, validation, or background-job execution.

### Frontend

The adaptive frontend renders only capabilities supported by metadata, evidence, permissions, and
policy. IPSP is the target identity; Domain Experience pages are dynamic views over generic
contracts, not separate hardcoded products.

### API, authentication, policy, and consent

FastAPI routes remain thin. Authentication, RBAC, project/dataset/column policy, outbound policy,
and runtime consent are enforced server-side before protected application services execute.

### Ingestion and storage

Structured/tabular inputs pass authorization, staging, validation, versioning, provenance, and
analytical registration. Storage uses the frozen SQLite control plane and source/Parquet analytical
plane.

### Data Understanding

Deterministic profiling establishes types, grain, entities, time, measures, units, currencies,
relationships, observation maturity, sensitive data, availability, and lineage. Names are evidence,
not truth.

### Semantic and Metric Layer

The Dataset Semantic Manifest is the versioned dataset authority. The Metric & Formula Registry owns
generic numerical definitions and validated computation; Domain Experiences request semantic metric
IDs rather than embedding formulas.

### Domain Experience and Cross-Domain Composition

Registered Domain Experience Packs extend IPSP Core with vocabulary, objectives, prerequisites,
controls, and presentation metadata. The CrossDomainSemanticGraph represents evidence-backed entity,
grain, time, unit, currency, and transformation relationships. Ambiguous relationships require
confirmation; arbitrary joins are prohibited.

### Capability Discovery

Capability Discovery decides what the semantic and data evidence can responsibly support before an
engine is selected. Unsupported paths remain limited, disabled, blocked, or refused with reasons.

### Scenario, evidence, and engine/license resolution

ScenarioIntentManifest records the governed request, evidence access, assumptions, constraints, and
consent. EngineRegistry, LicenseRegistry, and EngineResolver then select only installed, eligible,
licensed, validated providers. Provider libraries remain replaceable adapters.

### Composite Simulation Graph

CompositeSimulationGraph is the universal execution abstraction for deterministic formulas,
statistical/ML/time-series/causal models, Monte Carlo, optimizers, synthetic support, benchmarks,
analogs, external evidence, user assumptions, and constraints. Its edges distinguish deterministic,
observed, predictive, causal, assumed, prior, and constraint relationships.

### Trust, Evidence Profile, results, and learning

Trust and Evidence Profile are separate authorities. Persisted outputs support history, compare,
re-run, reproduce, and authorized export. SimulationLearningStore and OutcomeReconciliation retain
experience and later actual outcomes behind learning-eligibility and promotion gates; simulated or
synthetic data never silently becomes observed truth.

## Cross-cutting architecture

Every layer preserves:

- security, authentication, RBAC, and project/dataset/column policy;
- privacy, outbound policy, runtime consent, and secret references;
- provenance and evidence authority;
- provider, dependency, solver, and model-weight licensing;
- observability, trace propagation, safe errors, and durable audit;
- background jobs, cancellation, ownership, and safe artifact references;
- versioning, reproducibility, and immutable referenced contracts;
- typed configuration and fail-closed security defaults.

## Storage planes

### Control, governance, and knowledge plane — SQLite

SQLite stores identities, permissions, configuration references, project/dataset metadata, semantic
and metric contracts, registry records, jobs, model/run metadata, Trust/Evidence records, audit, and
learning eligibility. SQL access remains repository-owned and synchronous under the accepted
foundation decisions.

### Analytical data plane — source files and Parquet

Immutable originals, canonical structured datasets, validated analytical views, training-data
references, and simulation artifacts remain outside the SQLite control plane. SQLite is not the
mandatory warehouse for large analytical row sets.

## Provider and portability boundaries

Application services depend on IPSP interfaces. Engine, storage, job, LLM, evidence, reporting, and
secret implementations remain replaceable providers subject to capability, license, security,
resource, and Trust gates. Candidate provider names in architecture documents do not assert an
installed dependency.

## Current implementation boundary

v0.1.0 implements the secure FastAPI/SQLite foundation, authentication/RBAC, sessions/CSRF,
configuration/secrets/outbound boundaries, jobs, observability/audit, health, and offline static UI.
The analytical layers described above remain planned until their roadmap milestones are separately
implemented, tested, independently reviewed, and accepted. v0.2.0 remains not started.
