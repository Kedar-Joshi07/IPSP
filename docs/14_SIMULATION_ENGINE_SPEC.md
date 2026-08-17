# Simulation Engine Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.8.0 — Simulation Core + ScenarioIntentManifest +
CompositeSimulationGraph foundation

This specification freezes the universal simulation bases, the versioned `ScenarioIntentManifest`,
and the common validation boundary. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and does not create runtime services,
tables, APIs, providers, or dependencies.

## Exact canonical simulation bases

The complete set of top-level simulation bases is exactly:

- `DATA_BASED`
- `MIXED`
- `INTENT_BASED`

No fourth canonical basis is permitted.

`DATA_BASED` relies primarily on observed or derived first-party data and validated formulas or
models. `MIXED` combines empirical evidence with explicitly identified assumptions, analogs,
benchmarks, synthetic support, or external evidence. `INTENT_BASED` begins from a user objective
when empirical support may be incomplete and must expose every material assumption and limitation.

The basis describes the scenario's evidence foundation. Predictive scoring, deterministic what-if,
Monte Carlo, optimization, stress testing, benchmark/analog use, and synthetic support are engine or
graph-node patterns and evidence mechanisms; they are not additional bases. Intent-based output
never masquerades as observed truth.

## ScenarioIntentManifest

The `ScenarioIntentManifest` is the versioned authority for what a user is asking the system to
evaluate. It is distinct from both the execution graph and the result. Each version conceptually
records:

| Contract area | Required meaning |
|---|---|
| Identity | Stable manifest ID, manifest version, contract version, author/actor, creation time, and supersession reference |
| Context | Project/workspace, dataset/table versions, Dataset Semantic Manifest versions, activated Domain Experience versions, and organization configuration version |
| Basis | Exactly one canonical simulation basis and the evidence-based reason it applies |
| Domains | One or more activated domain families, including Composite/Cross-Domain only when supported |
| Objective | Objective, requested outcome, decision question, and comparison intent |
| Scope | Horizon, event/as-of time, time zone, calendar/fiscal context, geography, and population or entity scope |
| Resources and goals | Available resources, targets/goals, and priorities |
| Uncertainty preference | Requested interval, distribution, sensitivity, risk, confidence, or deterministic treatment and communication preference |
| Controls | Proposed decision/control variables, baseline values, scenario values/ranges, units, timing, and eligibility evidence |
| Constraints | Intrinsic, confirmed semantic, business, policy, resource, and other validated constraints with references |
| Assumptions | Explicit typed assumptions, values/ranges/distributions, units, source/provenance, owner, rationale, sensitivity, and confirmation state |
| Comparison basis | Baseline, plan, actual, forecast, prior scenario, benchmark/analog, or other supported reference with exact version and alignment semantics |
| Evidence | Evidence references, evidence cutoff/snapshot, requested evidence-access mode, evidence gaps, and provenance classes |
| Consent and policy | Effective consent/evidence-access snapshot plus privacy, outbound, permission, and policy references; never credentials or secret values |
| Requested output | Measures, metrics, segments, uncertainty, explanation, comparison, and precision requirements |
| Validation | Semantic/capability/support findings, ambiguities, confirmations, limitations, refusal reasons, and Trust requirements |
| Reproducibility | Metric, graph, model/engine/provider, seed, policy, configuration, and other version requirements known before execution |

These are conceptual contract fields, not persistence-table columns.

### Lifecycle and immutability

The conceptual lifecycle is:

```text
capture draft intent
  → validate structure, semantics, permissions, evidence, and capability
  → clarify or confirm material ambiguity and assumptions
  → freeze an immutable manifest version
  → compile and validate an eligible CompositeSimulationGraph, or refuse
  → execute against the frozen manifest version
  → retain result, Trust, Evidence Profile, and reproducibility references
```

A material change to basis, objective, scope, control, constraint, assumption, evidence-access or
consent snapshot, comparison basis, or requested output creates a new manifest version. A completed
run always references the immutable version it used. Exact lifecycle enums, persistence tables, API
resources, and storage mechanics are deferred to later contract freezes.

## Engine and node patterns

Patterns remain composable and may coexist inside one validated graph:

- **Deterministic formula/accounting:** evaluate confirmed Metric & Formula Registry definitions,
  identities, allocations, conversions, or reconciliations.
- **Statistical, ML, time-series, or causal model:** score only with a validated eligible model;
  predictive association is not presented as causal effect, and causal execution requires the
  separate causal gate.
- **Monte Carlo:** propagate supported uncertainty through validated distributions, residuals, or
  assumptions; intervals require meaningful calibration and lineage.
- **Optimizer:** search over validated decision variables and constraints only after objective,
  feasibility, relationship, license, resource, and Trust gates pass.
- **Synthetic generator/support:** use a provider-neutral synthetic interface with complete
  `SYNTHETIC_DATA` provenance; synthetic context does not decide outcomes or become observed truth.
- **Benchmark, analog, or external evidence:** use as a qualified prior, comparison, or assumption
  with applicability and provenance, never as first-party observation.
- **User assumption or constraint:** represent explicitly in the graph with validation, sensitivity,
  and evidence dependence visible in the result.

Provider eligibility and deterministic selection are governed by the
[Engine & License Registry Specification](48_ENGINE_LICENSE_REGISTRY_SPEC.md).

## Control, constraint, and outcome eligibility

A field or semantic concept can be a scenario control only when the Dataset Semantic Manifest and
capability evidence identify it as controllable, or when explicit assumption mode is allowed and
clearly labeled. IDs, outcomes, post-outcome variables, unavailable-at-decision-time features, and
unsafe sensitive features are not ordinary controls.

Outcome, control, feature, and evidence timing must respect the prediction horizon. Same-period or
post-outcome derivations cannot create circular predictive evidence. Constraints retain their class,
source, confirmation state, units, and enforcement behavior; empirical expectations remain warnings
unless confirmed and promoted through governance.

## Support and extrapolation

Every applicable scenario path evaluates:

- historical range and population/entity support;
- combination, cohort, and relationship support;
- extrapolation distance and direction;
- observation maturity and evidence freshness;
- missing or ambiguous required context;
- grain, unit, currency, time/calendar, and semantic compatibility;
- intrinsic, confirmed, business, policy, and resource constraints.

Unsupported paths are limited, blocked, or refused with reasons. Amber may expose a qualified result
only when no hard gate fails and the limitation is explicit. A graph is never completed by inventing
an edge, conversion, formula, distribution, or effect.

## Result and reproducibility boundary

Execution produces a persisted Run Result Object with the exact manifest and graph versions,
selected engines/models/providers, metric definitions, evidence snapshot, assumptions, conversions,
constraints, random seeds, non-secret configuration, Trust, Evidence Profile, warnings, and lineage.
Re-run and reproduce follow the separate
[Simulation History & Reproducibility specification](26_SIMULATION_HISTORY_REPRODUCIBILITY.md).

Composite execution is governed by the
[Composite / Cross-Domain Simulation Specification](49_COMPOSITE_CROSS_DOMAIN_SIMULATION_SPEC.md).
Trust and Evidence assessment are governed by the
[Trust & Validation Specification](15_TRUST_AND_VALIDATION_SPEC.md).
