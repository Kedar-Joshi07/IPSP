# Glossary

**F-002** — The authoritative post-v0.1.0 architecture freeze. It is an architecture identifier,
not application v2.0 and not evidence that a frozen capability is implemented.

**Capability** — An analytical, predictive, simulation, optimization, explanation, comparison, or
learning function that evidence and policy show a dataset can responsibly support.

**Dataset Semantic Manifest** — Versioned contract describing dataset grain, fields, entities,
semantics, relationships, constraints, metrics, capabilities, confirmations, and provenance.

**Domain Experience Pack** — A registered extension that supplies domain vocabulary, objectives,
semantic concepts, metric requests, controls, UI metadata, explanations, and prerequisites without
forking IPSP Core or owning generic numerical truth.

**Domain Experience Manifest** — The versioned declaration of a Domain Experience Pack's identity,
compatibility, vocabulary, objectives, semantic/capability prerequisites, requested metric IDs,
controls, constraints, and presentation metadata.

**CrossDomainSemanticGraph** — A validated graph of cross-domain concepts and their entity, grain,
time, unit, currency, transformation, evidence, and support relationships.

**Metric & Formula Registry** — Versioned authority for semantic metric identities, inputs,
formulas, aggregation/time/grain/unit behavior, validation, lineage, and provenance.

**EngineRegistry** — Registry of execution providers, versions, capabilities, availability,
resource needs, and security metadata.

**LicenseRegistry** — Registry of dependency, provider, solver, commercial-use, redistribution,
service, and model-weight license constraints.

**EngineResolver** — Deterministic policy component that selects only capability-valid, licensed,
trusted, data-suitable, available providers according to organization policy.

**ScenarioIntentManifest** — Versioned scenario request containing domains, objective, outcome,
horizon, geography, population/entity, resources, goals, controls, constraints, assumptions,
comparison basis, uncertainty preference, evidence access, and consent snapshot.

**CompositeSimulationGraph** — Universal execution abstraction whose typed nodes perform formulas,
models, simulation, optimization, evidence transforms, assumptions, or constraints and whose edges
state the defensible relationship type.

**Evidence Profile** — Description, separate from Trust, of a result's dependence on observed data,
actual outcomes, assumptions, synthetic data, analogs, external evidence, extrapolation, freshness,
and coverage.

**SimulationLearningStore** — Governed store for scenario experience, evidence, outputs, user
actions, corrections, and later outcomes that remains logically separate from empirical analytical
data.

**OutcomeReconciliation** — Process that connects a simulation at T0 with a later observed outcome
at T1, compares expected and actual results, attributes error, and produces a governed learning
candidate.

**Observed outcome** — A later real-world result with sufficient identity, time, grain, provenance,
and lineage to reconcile against a prior scenario; it is distinct from simulated output.

**Synthetic provenance** — Generator, provider, version, seed, configuration, quality, privacy, and
lineage metadata that prevents synthetic records from silently becoming observed truth.

**Evidence access mode** — Governed scope for retrieval: `OFF`, `INTERNAL_ONLY`, `PUBLIC_WEB`, or
`APPROVED_CONNECTORS`, further constrained by Admin policy, project/dataset policy, and runtime
consent.

**Control plane** — SQLite metadata, knowledge, governance, registry, and operational state.

**Analytical data plane** — Source and Parquet datasets and artifacts used for computation.

**Champion/Challenger** — Controlled model lifecycle in which validated candidates compete before
promotion; no model self-promotes from a single simulation.

**Prediction horizon** — When a prediction is made relative to feature and outcome availability.

**Feature lineage** — How a feature is derived, transformed, binned, or aggregated from other data,
including temporal availability.

**Intrinsic constraint** — A mathematically unavoidable validity rule.

**Business constraint** — An explicit confirmed process or business rule, not universal numerical
truth.

**Attribution** — Assignment under a declared rule; not proof of causal effect.

**Look-alike** — Similarity to a seed cohort; distinct from calibrated response propensity.

**Trust** — Evidence-backed validation of data, semantics, relationships, models, leakage, support,
constraints, privacy, licensing, and reproducibility. It is separate from the Evidence Profile and
from model or LLM confidence.
