# Product Requirements

## Status boundary

These are target requirements governed by the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md). The accepted v0.1.0 implementation is
limited to its verified foundation behavior. v0.1.1 reconciliation is in progress, v0.2.0 is not
started, and a target requirement is not an implementation claim.

## Functional requirements

### Authentication and governance

- Local username/password authentication.
- Admin and User roles backed by granular permissions.
- Project, dataset, and column-sensitive policy where applicable.
- User activation/deactivation, password change, failed-login lockout, and session expiry.
- Runtime consent and outbound-policy enforcement for external evidence or providers.
- Provider, dependency, solver, and model-weight license decisions remain explicit and auditable.

### Project and dataset lifecycle

- Project/workspace parent object.
- Structured/tabular dataset upload, staging, validation, versioning, and archive/delete with
  dependency checks.
- Dataset provenance distinguishing full data from random, stratified, time-window, filtered, or
  aggregated samples.
- Optional original row count and original time coverage.
- Immutable originals and versioned analytical references in the two-plane storage model.

### Understanding and semantic contracts

- Column profiles, missingness, sentinels, cardinality, distributions, and safe examples.
- Candidate identifiers, entities, grain, dimensions, measures, outcomes, controls, time, and
  helper fields.
- Units, currencies, calendars, fiscal periods, and availability time where supported.
- Hierarchies, functional dependencies, relationship cardinalities, and multi-table proposals.
- Feature lineage, derived/binned/aggregate fields, and semantic redundancy.
- Sensitive and quasi-identifier classification.
- Clarification questions, persisted confirmations, conflicts, and new manifest versions.
- A versioned Dataset Semantic Manifest that supports metrics, Domain Experience activation,
  Cross-Domain relationships, capability discovery, scenario intent, Trust/Evidence, and learning
  eligibility.

### Domain Experience and metric requirements

- IPSP Core remains domain-neutral and composes with registered Domain Experience Packs.
- Target families include Marketing, Product, Sales, Customer Experience, Finance,
  Operations/Demand, Generic/Custom, and Composite/Cross-Domain.
- A Domain Experience Manifest declares vocabulary, objectives, semantic prerequisites, requested
  metric IDs, controls, constraints, UI metadata, explanations, and compatibility without imposing
  physical source columns.
- Numerical metric truth belongs to a versioned Metric & Formula Registry, not a Domain Experience.
- Organization configuration, observed or confirmed dataset values, curated packs, and explicit
  user assumptions follow the frozen precedence order.
- Finance activates only from evidence and does not impose one schema on generic core.

### Cross-Domain composition

- CrossDomainSemanticGraph relationships record concepts, entities, grain, time, units, currency,
  transformation, evidence, and support status.
- Cross-domain composition reconciles entity and aggregation grain, time zones, calendar/fiscal
  periods, currencies, and units.
- Ambiguous relationships follow infer → validate → confirm when ambiguous → persist.
- Arbitrary joins and unsupported composite paths are prohibited.

### Capabilities, engines, and modelling

- Discover descriptive, diagnostic, predictive, similarity, forecasting, deterministic what-if,
  sensitivity, Monte Carlo, risk/stress, synthetic-assisted, optimization, causal, and composite
  capabilities only where supported.
- Capability validity is determined before provider selection.
- Baselines are required; model candidates depend on semantics, data, horizon, temporal structure,
  explainability, uncertainty, resources, license policy, and comparative validation.
- EngineRegistry records provider capability and availability; LicenseRegistry records dependency
  and model-weight restrictions; EngineResolver selects only eligible providers.
- Provider libraries remain adapters behind IPSP interfaces and are never hardcoded as the generic
  architecture.
- Prediction, attribution, causation, simulation, and optimization remain distinct.

### Scenario and simulation

- Dynamic controls derive from validated capability and semantic metadata.
- The exact scenario bases are `DATA_BASED`, `MIXED`, and `INTENT_BASED`.
- ScenarioIntentManifest records domain, objective, outcome, horizon, population, controls,
  constraints, assumptions, comparison basis, uncertainty preference, evidence access, and consent.
- CompositeSimulationGraph represents execution nodes and explicitly typed relationships.
- Learned predictive controls remain distinguishable from user assumptions.
- Support checks and extrapolation warnings precede execution.
- Uncertainty outputs such as P10/P50/P90 are shown only when justified.
- Unsupported paths are limited, disabled, blocked, or refused with reasons.

### Trust and Evidence Profile

- Trust evaluates data, semantics, relationships, model validation, leakage, support,
  extrapolation, constraints, accounting reconciliation, unit/currency/time consistency, privacy,
  outbound policy, licensing, and reproducibility.
- Evidence Profile separately reports dependence on observed data, actual outcomes, assumptions,
  synthetic data, analogs, external evidence, extrapolation, freshness, and coverage.
- Neither LLM confidence nor model confidence substitutes for Trust or evidence validation.

### Results, history, and governed learning

- Dynamic metrics, tabs, charts, warnings, model/data support, and Evidence Profile presentation.
- PDF and Excel exports generated from persisted, authorized result data.
- Run history, compare, re-run, and exact reproduce behavior.
- SimulationLearningStore keeps scenario experience separate from empirical analytical data.
- OutcomeReconciliation links a simulation at T0 to a later observed outcome at T1.
- Learning candidates pass eligibility, provenance, leakage, validation, Trust, challenger, and
  promotion gates; a simulation never directly becomes empirical truth or retraining data.

### Administration and operations

- AI/evidence provider configuration and exact LLM modes: `ML_ONLY`, `LOCAL_LLM`, `REMOTE_LLM`,
  and `HYBRID_LLM`.
- Exact evidence-access modes: `OFF`, `INTERNAL_ONLY`, `PUBLIC_WEB`, and `APPROVED_CONNECTORS`.
- Internet/outbound policy, runtime consent, and SecretProvider references.
- Engine/license registry policy and model lifecycle controls.
- Logs, trace IDs, jobs, health, backup/retention, and safe actionable errors.

## Non-functional requirements

- Generic production logic remains dataset/schema and domain agnostic.
- Raw dataset rows are not sent to a remote LLM by default.
- Results are reproducible from versioned data, semantics, metrics, models, providers, scenarios,
  evidence, seeds, and non-secret configuration.
- Security, privacy, provenance, licensing, observability, and responsible refusal are cross-cutting.
- The product remains useful in `ML_ONLY` mode.

## Bounded v1.0 requirement

v1.0 is the first complete, production-usable IPSP expression. It requires the core structured-data,
semantic, Domain Experience, metric, capability, modelling, simulation, Trust/Evidence, history,
learning-foundation, local-AI-assistance, export, and dynamic-UI contracts frozen by F-002.

Advanced production causal workflows, full solver-backed optimization, automatic LLM fine-tuning,
Remote/Hybrid LLM execution, public-web evidence, enterprise connectors and scale, and specialized
Quant Finance are not mandatory v1.0 blockers when their architecture boundaries remain intact.
