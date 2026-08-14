# Model Registry & Lifecycle Specification

## Status and authority

This planned F-002 contract defines model identity, evidence, and governed promotion. It does not
implement training, persistence, serving, or automatic promotion in v0.1.1.

## Canonical statuses

- `TRAINING`
- `CANDIDATE`
- `CHALLENGER`
- `CHAMPION`
- `REJECTED`
- `ARCHIVED`

Exact transition persistence is deferred, but no implementation may silently skip evidence gates or
self-promote after a request or simulation.

## Registry metadata

Each model version conceptually records:

- stable model ID, version, status, parent, challenger/champion relationship, and timestamps;
- capability ID/version, objective, outcome semantics, output type, entity/population, and horizon;
- dataset/table versions and training/evaluation data references;
- Dataset Semantic Manifest, Metric & Formula Registry, Domain Experience, and relationship/graph
  versions;
- feature set, complete feature lineage, availability-time evidence, transformations, and exclusions;
- engine family, EngineRegistry provider ID/version, library/runtime version, and artifact format;
- Runtime Engine Inventory snapshot and resource/hardware requirements;
- dependency license, solver/commercial license where applicable, and model-weight license;
- split/backtest strategy, baseline, candidate set, random seed, and non-secret configuration hash;
- task metrics, baseline comparison, segment/time stability, robustness, and support evidence;
- probability calibration method/evidence where applicable;
- uncertainty/interval method and coverage evidence where applicable;
- explainability method, limitations, and artifact references;
- Trust result, constraints, privacy/security policy, promotion evidence, approvals, and reason codes;
- artifact checksum/location reference, reproducibility environment, and provenance.

Physical source fields are referenced through exact Semantic Manifest/lineage contracts rather than
becoming fixed registry schema.

## Lifecycle

```text
TRAINING
  → CANDIDATE
  → CHALLENGER
  → CHAMPION
```

At any eligible stage a version may become `REJECTED` or `ARCHIVED`. A prior champion remains
reproducible after replacement. Rollback selects an eligible immutable prior version; it does not
rewrite history.

## Candidate and challenger gates

A candidate must demonstrate:

- valid semantic/data capability and provider/license eligibility;
- leakage-safe training and validation data;
- meaningful baseline comparison;
- required calibration, uncertainty, explainability, and constraint evidence;
- resource, latency, security, privacy, and reproducibility suitability;
- complete lineage, artifacts, and Trust evidence.

A challenger competes against the current champion using predefined metrics and acceptance evidence,
including performance, calibration, stability, segment behavior, support, constraints, latency,
resources, license, and policy. No single aggregate score automatically wins.

## Champion promotion

Promotion requires explicit governed evidence and authorization. It records:

- compared versions and evaluation datasets/windows;
- baseline and champion deltas with uncertainty where meaningful;
- calibration, drift/stability, robustness, segment, support, and constraint results;
- provider/license/security/resource eligibility at promotion time;
- Trust outcome, approver, decision, reasons, and effective time.

Failure of a mandatory semantic, leakage, license, security, constraint, or reproducibility gate
blocks promotion regardless of predictive score.

## Shadow evaluation and observed outcomes

A challenger may receive equivalent requests without serving its output. When sufficiently matched
observed outcomes later exist, governed reconciliation can compare versions. Simulated results,
intent-based assumptions, synthetic records, or LLM proposals do not become observed outcomes.

Detailed SimulationLearningStore and OutcomeReconciliation behavior belongs to F2-F.

## Learning policy

Models improve through governed training-dataset construction, batch retraining by default,
challenger evaluation, Trust validation, and explicit promotion/rejection. One request or simulation
never directly rewrites model weights or champion state. True incremental learning requires a later
contract proving genuine streaming semantics and equivalent governance.

## Reproducibility

Reproduction resolves exact data, semantic, metric, relationship, feature-lineage, engine/provider,
library, license, artifact, configuration, seed, validation, Trust, and policy references. A missing
or no-longer-eligible provider is reported honestly; the registry does not silently substitute a
different engine for historical reproduction.
