# Composite / Cross-Domain Simulation Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.8.0 foundation with v0.10.0 Cross-Domain completion

This specification freezes the `CompositeSimulationGraph` execution contract and its relationship
to the semantic authorities. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md), the
[Simulation Engine Specification](14_SIMULATION_ENGINE_SPEC.md), and the
[Domain Experience Pack Specification](47_DOMAIN_EXPERIENCE_PACK_SPEC.md). It does not implement a
graph engine, provider adapter, API, persistence schema, or Domain Experience.

## Governing boundary

The versioned `ScenarioIntentManifest` states **what** is requested. The versioned
`CrossDomainSemanticGraph` states **which semantic relationships are supported**. The versioned
`CompositeSimulationGraph` states **how validated nodes and relations execute** for that request.

```text
ScenarioIntentManifest
  + Dataset Semantic Manifest(s)
  + CrossDomainSemanticGraph
  + capability, metric, engine, license, policy, and evidence decisions
  → validate and compile CompositeSimulationGraph
  → execute, limit, block, or refuse
  → Run Result Object + Trust + Evidence Profile + lineage
```

The execution graph cannot create semantic authority. No arbitrary join, formula, conversion,
effect, dependency, or graph edge may be invented to satisfy user intent.

## Graph identity and versioning

Each graph version conceptually records:

- stable graph ID, immutable graph version, contract version, creation time, and supersession;
- exact ScenarioIntentManifest and canonical simulation basis;
- project/workspace, dataset/table, and Dataset Semantic Manifest versions;
- activated Domain Experience and CrossDomainSemanticGraph versions;
- Metric & Formula Registry definition/dependency versions;
- capability decisions and selected model/artifact versions;
- EngineRegistry, Runtime Engine Inventory, EngineResolver, and LicenseRegistry decisions;
- evidence cutoff/snapshot, consent/evidence-access snapshot, policy and non-secret configuration;
- graph nodes, edges, declared inputs/outputs, execution plan, validation result, and canonical hash;
- Trust requirements, assumptions, constraints, limitations, and refusal reasons.

A completed or accepted result references an immutable graph version. Any material change to a node,
edge, dependency, assumption, constraint, conversion, evidence reference, execution ordering, or
governance snapshot creates a new graph version. Exact serialization and persistence are deferred.

## Node types

The graph supports typed nodes whose eligibility and provider requirements remain explicit:

1. **Input/evidence reference** — frozen observed, derived, configuration, outcome, prior-run,
   benchmark, external, local-knowledge, or synthetic evidence reference.
2. **Deterministic formula/accounting** — versioned metric definition, identity, allocation,
   conversion, roll-forward, or reconciliation.
3. **Statistical / ML / time-series / causal model** — validated model execution with the task and
   causal meaning kept explicit.
4. **Monte Carlo** — supported uncertainty propagation with distribution, dependency, seed, and
   calibration references.
5. **Optimizer** — governed objective, decision variables, constraints, feasibility, and selected
   solver/provider.
6. **Synthetic generator/support** — provider-neutral generation or augmentation with full
   `SYNTHETIC_DATA` provenance and no promotion to observed truth.
7. **Benchmark or analog** — qualified comparison/prior with population, period, unit, applicability,
   license, and limitation evidence.
8. **External-evidence transform** — governed transformation of cited external evidence under the
   frozen evidence-access and consent snapshot.
9. **User assumption** — explicit typed value, range, distribution, relation, or scenario-only
   premise with source, confirmation, sensitivity, and scope.
10. **Constraint** — intrinsic, confirmed semantic, business, resource, feasibility, or policy rule
    applied to specified nodes/outputs.

An implementation may define compatible subtypes, but it cannot add a node that bypasses these
authorities or silently changes evidence meaning.

### Common node contract

Each node conceptually declares identity/version, type, semantic concept and domain context, typed
inputs/outputs, entity and aggregation grain, event/as-of time, window/calendar/fiscal semantics,
unit/currency/scale, stock/flow behavior, evidence/provenance, capability and provider resolution,
parameters and seed behavior, constraints, support limits, validation, Trust requirements, and safe
failure behavior.

Node inputs and outputs are references to typed semantic/metric contracts, not mandatory physical
source-column names. A node cannot read an undeclared upstream value or use information unavailable
at the required decision time.

## Edge semantics

Every edge has exactly one declared semantic relation type from the frozen set:

- **deterministic relation** — a validated identity, formula, transformation, allocation, or
  reconciliation;
- **observed association** — an empirical association that does not imply intervention or causality;
- **predictive relation** — a validated predictive mapping for an exact target, horizon, and support;
- **causal estimate** — an estimate that passed the separate causal-identification gate and retains
  assumptions, diagnostics, and scope;
- **assumption** — an explicit scenario-only dependency supplied or confirmed as an assumption;
- **external prior** — qualified dependence on external evidence;
- **analog prior** — qualified dependence on a curated benchmark or analog population;
- **constraint** — a directed applicability/enforcement dependency, not an effect estimate.

An edge conceptually includes source/target ports and nodes, direction, relation meaning, entity and
grain mapping, cardinality and coverage, event/availability-time relationship, window/lag/calendar,
unit/currency/scale/stock-flow compatibility, transformation/reconciliation reference, evidence and
provenance, support/extrapolation bounds, assumption or causal qualifications, version, validation,
and Trust requirements.

Name similarity, correlation, model feature importance, a Domain Experience hint, benchmark story,
LLM proposal, or user desire cannot independently establish an edge. Every execution edge must map
to a validated semantic relationship or to an explicitly typed assumption/prior/constraint allowed
by the frozen intent. If no defensible relation exists, the path is constrained or refused.

## Execution ordering and dependencies

The compiled graph has explicit declared inputs/outputs and a deterministic dependency plan:

1. resolve immutable contract and evidence references;
2. validate graph structure, semantics, policies, and providers;
3. establish a stable topological execution order with deterministic tie-breaking;
4. evaluate inputs, assumptions, conversions, and prerequisite deterministic nodes;
5. execute eligible model, Monte Carlo, synthetic-support, or optimizer nodes;
6. enforce constraints at their declared pre-node, post-node, and final-output boundaries;
7. perform deterministic/accounting reconciliations and Trust checks;
8. persist result, partial/refused paths, Evidence Profile, and complete lineage.

An undeclared cycle is invalid. A mathematically iterative process must be encapsulated in an
eligible typed node with declared initialization, convergence/termination, maximum work, seed/
determinism, failure behavior, and provider support; it does not authorize a cyclic graph dependency.
Independent eligible branches may run in parallel only when the frozen plan preserves deterministic
inputs, resource policy, seeds, ordering-sensitive behavior, and audit lineage.

## Graph validation

Validation occurs before execution and again for applicable outputs. It covers:

- schema/contract validity, immutable references, unique node/edge identity, declared ports, and
  acyclicity;
- node capability, model, provider, license, security, resource, and configuration eligibility;
- edge support in the semantic authorities or explicit intent assumption/prior/constraint authority;
- entity identity, grain, cardinality, join coverage, aggregation, and measure-multiplication risk;
- event and availability time, horizon, lag, time zone, business calendar, fiscal period, maturity,
  stock/flow, and leakage;
- dimensions, units, scale, denominators, currency, rate sources, and conversions;
- metric definitions, safe division, missing/sentinel behavior, constraints, and accounting
  reconciliation;
- evidence/provenance coverage, basis consistency, consent, privacy, outbound policy, and freshness;
- support, extrapolation, uncertainty/calibration, feasibility, and reproducibility completeness;
- output compatibility with the ScenarioIntentManifest and requested comparisons.

Validation produces structured reasons per graph, path, node, and edge. It never repairs a failure
by silently changing intent, basis, evidence class, relation meaning, provider, or formula.

## Domain crossing and reconciliation

Composite/Cross-Domain activation is evidence-driven and never guaranteed. A cross-domain path may
use only exact activated Domain Experience versions and validated `CrossDomainSemanticGraph`
relationships. Before execution, each boundary reconciles:

1. entity identity/mapping and entity grain;
2. source, target, aggregation, and output grain plus cardinality and deduplication;
3. event/as-of/availability time, horizon, lag, time zones, and period maturity;
4. calendar, business-calendar, and fiscal-period mappings;
5. units, dimensions, scale, denominator, and stock/flow behavior;
6. currency identity, rate source/type/effective time, direction, translation, and revaluation;
7. transformation, allocation, metric, and accounting lineage;
8. evidence, support, extrapolation, policy, license, and reproducibility.

A one-side measure is never directly aggregated after a one-to-many join without a validated safe
transformation to the required grain. Missing or ambiguous reconciliation requests targeted
confirmation where permissible; incompatibility limits or blocks the path.

## Assumptions, constraints, and evidence references

Assumption nodes make scenario-only premises visible. They declare applicability, owner/source,
typed value/range/distribution, unit/currency/time/entity scope, rationale, confirmation, provenance,
uncertainty, sensitivity, and expiry. An assumption cannot be relabeled as observed evidence.

Constraint nodes declare the governed class, expression/reference, scope, units, tolerance,
enforcement point, hard/qualified behavior, confirmation/policy authority, and reason. Empirical
expectations remain warnings unless promoted through confirmed governance. Optimizer constraints do
not establish causal or predictive response relations.

Evidence-reference nodes retain exact source/version, provenance class, cutoff/freshness,
population/grain/period, transformations, quality/applicability, privacy/license, access/consent, and
lineage. Synthetic, benchmark, prior-run, external, local-knowledge, and LLM evidence remain visibly
distinct from first-party observation and later observed outcomes.

## Failure, limitation, and refusal

Failures are scoped where safely possible:

- a non-essential unsupported branch may be omitted or limited only when the manifest permits a
  partial result and the omission is explicit;
- Amber paths may produce qualified outputs with visible assumptions, Evidence Profile dependence,
  extrapolation, and limitations;
- Red or mandatory failures block the affected path or whole result according to dependency and
  requested-output semantics;
- permission, privacy, outbound, license, invalid relation, intrinsic constraint, leakage,
  irreconcilable accounting/unit/currency/time/entity state, infeasibility, or absent required
  evidence causes refusal rather than fabrication;
- provider/runtime failure never triggers silent substitution; any allowed fallback requires a new
  recorded resolver result compatible with the frozen graph and reproduction semantics.

Partial results cannot imply that a blocked downstream output was evaluated. Safe reason codes,
remediation/clarification, trace IDs, and audit references are retained without exposing secrets or
raw stack traces.

## Deterministic and accounting reconciliation

Where deterministic identities or accounting relationships apply, the graph identifies authoritative
metric definitions, inputs, transformations, allocation/conversion rules, signs, stock/flow and
period semantics, tolerances, residuals, and reconciliation nodes. A predictive or simulated value
does not override a deterministic identity. Unexplained material imbalance is surfaced and blocks
claims that require reconciliation.

Accounting checks apply only when supported semantics establish the relationship; IPSP does not
invent an accounting identity or assume all monetary measures are non-negative. Scenario effects
remain separate from observed actuals and from subsequent outcome reconciliation.

## Support and extrapolation behavior

Support is evaluated per node, edge, path, and output. The graph retains population/cohort coverage,
combination support, model/domain applicability, evidence freshness, extrapolation direction and
distance, assumption/synthetic/analog dependence, and uncertainty. Limits may narrow controls,
remove optional outputs, require sensitivity analysis, mark Amber, or refuse. Extrapolation is never
silently represented as interpolation or first-party evidence.

## Result, Trust, Evidence, and reproducibility

The Run Result Object references the graph/manifest versions and captures node/edge outputs, blocked
and omitted paths, assumptions, constraints, uncertainty, reconciliations, selected providers,
metrics, evidence snapshot, Trust decomposition, separate Evidence Profile, lineage, warnings, and
audit trace.

Reproduction freezes graph and dependency versions, original evidence snapshot/cutoff, dataset and
semantic versions, Domain Experience/CrossDomainSemanticGraph versions, metric definitions,
models/artifacts, engine/provider/inventory/license decisions, seeds, assumptions, conversions,
constraints, policy/consent context, and non-secret configuration. An unavailable historical
component is reported honestly; it is not silently replaced.

## Deferred implementation detail

F2-E freezes the conceptual execution contract only. Graph serialization, APIs, persistence tables,
compilers/schedulers, caching, parallel runtime, provider adapters, tolerance catalogs, and UI require
their assigned later phases and accepted milestone contracts.
