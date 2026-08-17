# Simulation Learning & Outcome Reconciliation Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.12.0 — Learning + Outcome Reconciliation Foundation

This specification freezes the `SimulationLearningStore`, `OutcomeReconciliation`, learning
eligibility, governed training-data construction, and challenger/promotion boundaries. It is
subordinate to the [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md), the
[Model Registry & Lifecycle Specification](13_MODEL_REGISTRY_LIFECYCLE_SPEC.md), and the
[Simulation History & Reproducibility specification](26_SIMULATION_HISTORY_REPRODUCIBILITY.md). It
does not create runtime storage, schemas, APIs, training jobs, model providers, or automatic learning.

## Governing principle

```text
Every simulation becomes a learning experience;
not every simulation becomes empirical truth.
```

Learning uses explicit evidence authority, point-in-time lineage, validation, comparison, and human/
policy authorization. A request, run, user correction, generated record, retrieved passage, or LLM
proposal never directly changes a training dataset, model weight, champion, semantic contract, or
observed fact.

## Evidence-authority tiers

The ordered evidence-authority tiers are:

1. **Observed actual outcomes** — matched, mature, permitted `OBSERVED_OUTCOME` evidence.
2. **Derived observed data with lineage** — governed `DERIVED_DATA` whose observed sources and
   transformations remain complete and point-in-time valid.
3. **Data-based simulation experience** — `DATA_BASED` run experience; still simulated, not actual.
4. **Mixed simulation experience** — `MIXED` experience with empirical and assumption/prior support
   kept distinct.
5. **Intent-based simulation experience** — `INTENT_BASED` experience whose assumptions and limited
   empirical support remain explicit.
6. **LLM and other unverified proposals** — proposal/context only until a separate authority validates
   and reclassifies the underlying evidence through an authorized process.

Higher authority does not automatically mean fit for a particular objective, population, horizon, or
training use. Consent, privacy, license, semantic validity, leakage, quality, maturity, support, and
Trust gates still apply. Tier metadata is retained at record/feature/label/event scope where needed;
aggregation never hides a lower-tier dependency.

## SimulationLearningStore

The `SimulationLearningStore` is the governed memory of scenario and result experience. Each logical
learning record conceptually retains:

- stable learning-event/run/result identities, versions, actors, timestamps, and audit/trace;
- ScenarioIntentManifest, canonical basis, domains, Dataset Semantic Manifest, Domain Experience,
  CrossDomainSemanticGraph, and CompositeSimulationGraph versions;
- inputs, controls, constraints, assumptions, comparison basis, evidence snapshot, provenance classes,
  evidence-access and consent/policy snapshots;
- metrics/formulas, models/artifacts, engines/providers/licenses, seeds, non-secret configuration,
  outputs, uncertainty, reconciliations, support/extrapolation, Trust, and Evidence Profile;
- user actions, decisions, corrections, annotations, explanations, acceptance/rejection, and downstream
  action references where authorized;
- later candidate/matched observed outcomes, matching evidence, reconciliation result, errors,
  attribution/evaluation findings, and learning eligibility decisions;
- retention, privacy, license, reproducibility, supersession, and deletion/remediation state.

### Separation from empirical analytical data

The store is logically and access-control separated from source/Parquet analytical data and governed
empirical training datasets. Its simulated outputs, assumptions, synthetic records, user feedback,
and proposals are never exposed as ordinary observed rows through a convenience join, union, export,
or default repository query.

Training services consume only a versioned Training Dataset Builder artifact after the
LearningEligibilityGate passes; they do not train directly from the SimulationLearningStore. A later
observed outcome remains in its governed empirical/provenance authority and is linked by immutable
references rather than overwritten into the simulation record. Exact physical stores and tables are
deferred.

## User correction capture

A correction/feedback record conceptually includes actor and authority, target artifact/field/claim,
prior and proposed value, correction type, rationale, source evidence, provenance, privacy/license/
consent scope, time, confirmation/review, applicability, and supersession. Corrections may improve
semantic catalogs, prompts, explanations, assumptions, or learning candidates only through their
respective validators and owners.

A user's acceptance, edit, preference, rating, or repeated entry is not an observed outcome and does
not prove correctness. Conflicting corrections remain visible and follow source precedence; they are
not resolved by recency or majority alone.

## OutcomeReconciliation

`OutcomeReconciliation` connects a frozen prediction/simulation at T0 to a later real-world actual at
T1 without rewriting either history:

```text
simulation or prediction at T0
  → separately recorded real-world execution/action, when known
  → candidate observed actual at T1
  → deterministic actual-outcome matching and maturity validation
  → prediction/scenario versus actual comparison
  → error and model/assumption/evidence evaluation
  → governed learning candidate
```

### Actual-outcome matching

Matching conceptually requires:

- exact run/output and candidate `OBSERVED_OUTCOME` identities/versions;
- outcome/metric semantic equivalence and definition versions;
- entity/population identity, aggregation grain, cardinality, deduplication, and coverage;
- event, decision, horizon, availability/as-of and maturity time, time zone, calendar/fiscal period,
  late-arrival, restatement, and censoring semantics;
- units, scale, currency, conversion source/effective time, denominator, and stock/flow compatibility;
- intervention/execution status and exposure/assignment where needed, kept distinct from intent;
- source provenance, collection method, data quality, permission/consent, privacy, license, and
  retention eligibility;
- deterministic match rule/version, ambiguity, unmatched/multiple-match behavior, reviewer/confirmation,
  and audit lineage.

An intended control is not proof that an action occurred. A similarly named field, approximate date,
correlated value, or LLM suggestion cannot establish a match. Ambiguous, immature, missing, duplicate,
or semantically incompatible outcomes remain unmatched, limited, or rejected with reasons.

### Comparison and evaluation

Reconciliation preserves the original prediction, scenario basis, uncertainty, assumptions, graph,
evidence cutoff, model/provider, and Trust state. It records prediction/actual differences with the
applicable metric, units, tolerance, interval/calibration result, segment/time/support context, and
data revisions.

Error evaluation may distinguish data/label quality, semantic/matching error, model error, drift,
calibration, unsupported extrapolation, assumption error, external-evidence/analog weakness,
execution deviation, constraint/reconciliation failure, and irreducible uncertainty only when the
evidence supports that distinction. It does not infer causal impact from observational disagreement.

## LearningEligibilityGate

The gate evaluates each candidate event, row, feature, label, correction, or artifact before training
dataset construction. Its versioned decision records eligible, limited/manual-review, or rejected
behavior with reasons, evidence, owner, policy, and expiry/re-evaluation where applicable.

Mandatory checks include:

- authorized learning objective, capability, target/outcome semantics, population, grain, and horizon;
- evidence-authority tier and complete source/derivation/matching provenance;
- confirmed semantic/metric/relationship versions and point-in-time feature availability;
- observed-outcome validity, maturity, label quality, matching quality, and execution/exposure state;
- sampling/coverage, duplication, dependence, class/segment/time balance, support, drift, and freshness;
- privacy, sensitive/proxy-feature, consent/purpose, retention/deletion, outbound, and security policy;
- source-data/evidence/dependency/model-weight license and allowed training/adaptation use;
- exclusion of leakage, circular features/labels, post-outcome data, prohibited artifacts, and
  unsupported transformations;
- reproducibility, audit, Trust, and required human/owner approval.

A failed mandatory gate cannot be offset by sample size, predictive performance, user popularity,
model confidence, or an LLM recommendation.

## Explicit no-direct-promotion rules

The following never directly become observed truth, an empirical label, or an ordinary empirical
training row:

- intent-based outputs;
- mixed assumptions or outputs that depend on them;
- synthetic records;
- LLM-proposed numbers or labels;
- unverified external evidence.

The same prohibition applies to benchmark/analog priors, prior-run outputs, scenario assumptions, and
unmatched user corrections. These artifacts may support planning, evaluation design, challenger-only
experiments, robustness tests, or evidence-gap discovery when explicitly eligible, isolated, and
labeled. They never receive `OBSERVED_DATA` or `OBSERVED_OUTCOME` provenance merely by passing through
a transform, memory store, or repeated simulation.

## Training Dataset Builder

The governed builder receives only gate-approved immutable references and produces a versioned
training/evaluation dataset manifest. It conceptually records:

- objective/target, population, entity and row grain, horizon, observation and label windows, cutoff,
  inclusion/exclusion, sampling/weighting, and maturity rules;
- exact source/dataset/table, semantic/metric/relationship, provenance, feature, label, and outcome-
  match versions;
- point-in-time feature assembly, transformations, imputation, aggregation, deduplication, unit/
  currency/time reconciliation, and missing/sentinel behavior;
- train/validation/test/backtest grouping and temporal boundaries, leakage barriers, random seeds,
  deterministic hashes/checksums, builder/code/configuration versions, and environment;
- evidence-tier composition, synthetic/assumption/proposal exclusion or isolated experimental use,
  support/coverage, drift, class/segment distributions, and known dependencies;
- privacy/consent/purpose, retention/deletion, sensitive features, license, security, Trust, owner,
  approvals, and audit lineage.

Feature and label sources remain separable. A one-side measure is not directly aggregated after a
one-to-many join without grain/cardinality validation. Entity, group, temporal, repeated-event, and
prior-run dependencies are kept within compatible splits to prevent contamination.

## Leakage and provenance validation

Validation establishes what was knowable at each decision/prediction time. It rejects or explicitly
isolates post-outcome variables, future availability, revised/restated values unavailable at T0,
same-period target derivations, target encodings fitted across splits, entity/group duplicates,
outcome-conditioned sampling, reconciliation artifacts, and features created from the label or the
same simulation output.

Every training value traces through transformations to its original provenance class and source
version. Deriving or joining a lower-authority artifact does not elevate it. Unknown, conflicting, or
broken lineage blocks the affected candidate.

## Candidate training and challenger evaluation

Training creates immutable `CANDIDATE` versions under the Model Registry lifecycle. Meaningful
baselines are mandatory. An eligible candidate becomes a `CHALLENGER` only after schema, data,
semantic, leakage, provider/license, privacy/security, reproducibility, and initial Trust gates pass.

Evaluation compares the challenger with the current champion and applicable baselines using predefined
objective-appropriate evidence, including:

- predictive/forecast/task performance with uncertainty and practical significance;
- probability and interval calibration where applicable;
- temporal, entity, segment, cohort, and support stability;
- drift sensitivity and performance across relevant windows/regimes;
- robustness to missingness, perturbation, assumptions, outliers, and distribution shift where valid;
- leakage/refutation checks, constraint and accounting/unit/currency/time consistency where applicable;
- explainability, fairness/proxy behavior, privacy/security, latency/resources, provider/license,
  reproducibility, and Trust;
- shadow/holdout and reconciled mature observed-outcome evidence where sufficient.

No single aggregate score automatically wins. Uncertainty, multiple comparisons, sample dependence,
and operational cost/risk are considered where material.

## Champion comparison, promotion, rejection, and rollback

Promotion requires an explicit versioned decision identifying candidate/challenger/champion versions,
evaluation datasets/windows, metrics/tolerances, deltas/uncertainty, calibration, drift/stability,
robustness, segment/support, constraints, resource/provider/license/security, Trust, approver, reasons,
and effective time.

A mandatory failure rejects or returns the challenger for remediation regardless of headline
performance. An inconclusive challenger is not promoted. Rejection retains evidence and reason;
archival does not erase lineage. The prior champion remains reproducible after replacement. Rollback
selects a previously eligible immutable version under current safety/policy checks and does not rewrite
historical serving or promotion records.

## Drift, monitoring, and learning cadence

Monitoring distinguishes input/data-quality drift, semantic/schema change, feature/relationship drift,
label/outcome drift, prediction/performance drift, calibration drift, segment instability, support
change, assumption/evidence aging, and provider/policy change. Thresholds and windows are objective-
specific, versioned, and compared with data volume/maturity; drift alone does not identify cause or
automatically retrain/promote.

Governed **batch retraining is the default**. A sufficient batch of mature eligible outcomes supports
stable splits, comparative evaluation, and explicit promotion. One simulation or outcome never
directly updates weights.

River or another incremental provider is permitted only when genuine streaming semantics are proven:
ordered event-time observations, online availability, repeated updates, label-delay/maturity handling,
prequential or equivalent leakage-safe evaluation, checkpoint/version rollback, drift controls,
resource/license eligibility, and promotion governance equivalent to batch learning. Incremental
updates remain challengers until explicitly promoted; library availability never proves streaming
suitability.

## LLM and Local AI learning boundary

LLM memory, retrieval, training-event preparation, and optional PEFT/LoRA adaptation follow the same
provenance, privacy/consent, license, reproducibility, evaluation, and promotion principles. The
preferred order is retrieval/memory, curated training-event preparation, optional PEFT/LoRA
challenger, evaluation, then promotion/rejection.

LLM-generated labels, rationales, corrections, summaries, or numbers remain `LLM_PROPOSAL` unless a
separate deterministic/empirical authority validates the underlying fact. Fine-tuning does not grant
numerical authority. Local/remote model artifacts retain independent model-weight license decisions.

## Reproducibility, privacy, and audit

Learning and reconciliation artifacts preserve exact input/evidence snapshots, provenance and
authority tiers, policy/consent/privacy/license context, semantic/metric/graph/model/provider versions,
matching/gate/builder/evaluation rules, code/configuration/seeds, decisions, owners, checksums, and
audit/trace. Secrets are references only.

Reproducing an historical learning decision uses its original frozen state and reports unavailable or
currently prohibited dependencies honestly. Re-running applies current eligible state and records the
change set. Neither operation rewrites evidence class or historical champion state.

## Deferred implementation detail

F2-F freezes conceptual ownership, gates, and evidence behavior only. Exact persistence schemas,
repositories, APIs, matching algorithms, training builders/jobs, monitoring thresholds, model/LLM
pipelines, River integration, promotion workflows, and UI require later contract freezes and accepted
milestones.
