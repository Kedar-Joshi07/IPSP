# Trust & Validation Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.9.0 — Trust + Evidence + History + Comparison

This specification freezes the independent Trust authority, its conceptual Green/Amber/Red outcomes,
and the separate Evidence Profile. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and does not define a database schema,
API, universal numeric score, or runtime implementation.

## Governing principle

**AI proposes. Evidence validates. Rules constrain. Models compete. Humans arbitrate exceptions.
The system remembers the outcome.**

Trust is independent of model confidence, prediction probability, interval width, provider health,
or LLM confidence. Those facts may be inputs to applicable checks, but none is Trust by itself. A
human exception cannot waive an intrinsic impossibility, permission denial, license block, privacy
block, fabricated relation, or other mandatory refusal.

## Independent Trust dimensions

Trust is a decomposed, versioned assessment over the dimensions applicable to a specific capability,
scenario, graph path, result, or export:

| Dimension | Required assessment |
|---|---|
| Data quality | Completeness, validity, representativeness, sampling role, anomalies, maturity, freshness, and drift |
| Semantic confidence | Confirmed meaning, roles, grain, outcome/control semantics, ambiguity, and manifest compatibility |
| Relationship validity | Identity, cardinality, join coverage, duplication risk, lineage, and CrossDomainSemanticGraph support |
| Model/engine validation | Baselines, validation design, calibration/uncertainty, robustness, provider eligibility, and artifact compatibility |
| Temporal leakage | Prediction horizon, point-in-time availability, post-outcome/same-period derivation, split validity, and maturity |
| Support and extrapolation | Population/cohort/combination coverage, historical support, extrapolation distance, and applicability |
| Constraints | Intrinsic, confirmed semantic, business, resource, and policy constraint compliance and feasibility |
| Accounting reconciliation | Applicable identities, balance/flow continuity, allocations, tolerances, and unexplained residuals |
| Unit consistency | Dimensions, scale, denominators, conversions, and aggregation compatibility |
| Currency consistency | Currency identity, rate source/type/effective time, direction, and translation/revaluation treatment |
| Time and calendar consistency | Event/as-of time, horizon, window, time zone, business calendar, fiscal period, stock/flow, and period maturity |
| Simulation support | Basis validity, control eligibility, graph validity, assumption sensitivity, uncertainty, and node/edge support |
| Optimization feasibility | Objective, decision variables, constraints, feasible region, response validity, and solver outcome where applicable |
| Privacy | Data minimization, sensitivity, purpose, retention, and permitted raw/derived-data handling |
| Outbound policy | Admin, project/dataset, and runtime-consent intersection plus destination and payload eligibility |
| Licensing | Provider, dependency, model-weight, solver, dataset, benchmark, and external-evidence decisions where applicable |
| Reproducibility | Frozen references, seeds, evidence/policy/configuration snapshots, artifacts, and historical-provider availability |

Not every dimension applies to every operation. Applicability and any not-evaluated reason are
explicit; silently treating a required check as not applicable is prohibited.

## Check and outcome contract

Each check conceptually records its dimension, subject and scope, versioned rule, evidence, outcome,
reason code, severity, limitation/remediation, evaluator/version, policy context, timestamp, and
provenance. The aggregate Trust result retains dimension-level outcomes and must not hide a blocking
failure behind an average.

Conceptual outcomes remain:

- **Green:** every required applicable check passes within its frozen tolerance and no material
  limitation remains.
- **Amber:** no mandatory gate fails, but limited evidence, novelty, extrapolation, low support,
  assumption dependence, unresolved non-critical uncertainty, provider condition, or another
  review-worthy limitation remains.
- **Red:** a mandatory check fails, including critical ambiguity, invalid relationship/graph,
  leakage, intrinsic or confirmed constraint violation, accounting failure, permission/privacy/
  outbound/license block, invalid model/engine, infeasibility, irreproducibility where reproduction
  is required, or unsupported capability.

Red blocks the affected result, path, export, or action and preserves a safe reason. Amber permits
only the explicitly allowed qualified behavior with visible warnings. Exact scoring, weighting,
tolerance catalogs, and exception workflows require later contract freezes; a single universal
weighted score is not frozen here.

## Constraint classes

1. **Intrinsic constraint** — mathematically inherent, such as a probability in `[0, 1]`.
2. **Confirmed semantic constraint** — derived from confirmed meaning and versioned evidence.
3. **Business constraint** — an explicitly defined and authorized process or policy rule.
4. **Empirical expectation** — a historical pattern; warning-only unless confirmed and promoted.

Never turn `revenue >= 0` into a universal rule. A negative value is invalid only when intrinsically
impossible or contrary to a confirmed semantic/business constraint. Otherwise statistical evidence
may make it an anomaly or warning, but negativity alone does not make it erroneous.

## Specialized validation

### Models and uncertainty

Meaningful baselines and task-appropriate validation are mandatory. Representative diagnostics may
include MAE/RMSE/WAPE/R² for regression, precision/recall/F1/ROC-AUC/PR-AUC/calibration for
classification, and time-aware backtests, MAE/WAPE, and interval coverage for forecasting. Metric
choice, splits, thresholds, and tolerances depend on target semantics and are recorded rather than
universally hardcoded.

### Simulation and Composite/Cross-Domain execution

Applicable checks include manifest/basis validity, graph structure and relation support, execution
ordering, interval ordering, control eligibility, assumptions, constraints, uncertainty calibration,
support/extrapolation, temporal leakage, deterministic/accounting reconciliation, and unit, currency,
time/calendar, entity, and grain consistency. No Trust outcome can validate an invented graph edge.

### LLM-assisted output

LLM proposals require strict schema validation, deterministic evidence consistency, conflict
detection, policy and evidence-access checks, and user confirmation for unresolved semantics. An LLM
never gains numerical, semantic-approval, license, or Trust authority.

## Evidence Profile — separate authority

The Evidence Profile describes **what evidence a result depends on and how that evidence is
composed**. It neither duplicates Trust nor produces a replacement Trust score.

For an exact capability, scenario, graph, result, or claim, the versioned profile conceptually records:

- first-party observed-data and derived-data dependence, coverage, grain, period, and freshness;
- later observed-outcome evidence kept distinct from simulated or predicted output;
- organization configuration and confirmed semantic evidence;
- user assumptions, including materiality, sensitivity, and confirmation state;
- synthetic-data contribution with generator/provider metadata and quality/privacy evaluation;
- curated benchmark, analog, external-evidence, and local-knowledge contribution and applicability;
- prior IPSP run dependence and its original simulation basis;
- LLM-proposal contribution, always marked unverified until separately validated;
- extrapolation share/distance, unsupported gaps, evidence conflicts, and evidence cutoff;
- provenance references, licenses, consent/evidence-access snapshot, and lineage to graph nodes,
  edges, metrics, outputs, and claims.

Composition may be represented as categorized contributions, ranges, dependency flags, or coverage
measures where defensible. Percentages are used only when their denominator and computation are
defined. Evidence freshness or first-party share does not itself determine Green/Amber/Red; Trust
evaluates the validity and implications of the profile through its own checks.

## Persistence and presentation boundary

Run Result Objects and exports retain both the Trust decomposition and the separate Evidence Profile,
including warnings, blocked paths, applicability, and version references. Presentation must keep the
two authorities visibly distinct and must not summarize Amber or Red away.

Exact persistence tables, API payloads, calculation algorithms, tolerances, and UI components are
deferred to later phases and owning milestone contract freezes.
