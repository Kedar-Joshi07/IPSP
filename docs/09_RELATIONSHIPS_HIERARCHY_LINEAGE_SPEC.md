# Relationships, Hierarchy & Lineage Specification

## Status and purpose

This planned F-002 contract governs evidence-backed relationships within and across datasets and
domains. It preserves useful predecessor relationship categories while adding the reconciliation
requirements needed by the CrossDomainSemanticGraph. It does not implement joins or simulation
execution.

## Relationship categories

### Structural

One-to-one, one-to-many, and many-to-many relationships with declared direction and cardinality.

### Identity

Exact, normalized, derived, or canonical identity with match rules, coverage, collision evidence,
and confirmation state.

### Temporal

Same-entity or cross-entity relationships with direction, window, event/availability time, maturity,
and selection rule. Temporal association does not establish attribution or causation.

### Ordered journey

A stage/measure graph whose monotonicity depends on cohort, unit, measurement, re-entry, and process
semantics. IPSP never forces every ordered journey into a strict funnel.

### Lifecycle and state

Operational progression, transitions, exceptions, reversals, and terminal/non-terminal states.

### Measure dependency

Versioned algebraic, derived, qualified, allocation, or transformation relationships owned by the
Metric & Formula Registry.

### Plan versus actual

Planned, target, budget, scenario, forecast, and actual measures related only when entity, grain,
time, unit, currency, version, and comparison semantics reconcile.

### Commercial flow

Evidence-backed upstream/downstream business movement. The category is generic and does not grant a
predefined funnel, formula, join, or causal interpretation.

### Hierarchy

Strict functional hierarchy, soft hierarchy, ragged hierarchy, alternate hierarchy, and
cross-classification with effective-time and coverage evidence where relevant.

## Relationship record

A relationship proposal or confirmation conceptually records:

- source and target dataset/table/entity/concept references;
- relationship category, direction, cardinality, and identity/selection rule;
- source grain, target grain, required aggregation grain, and measure-duplication risk;
- event time, availability time, time zone, window, calendar, and fiscal-period relationship;
- source/target units and currencies plus validated conversion or reconciliation requirements;
- transformation or mapping reference;
- evidence, coverage, confidence, ambiguity, confirmation, and support status;
- provenance, contract version, and supersession references.

Physical source fields remain mappings inside a Dataset Semantic Manifest; a relationship contract
does not require domain-specific source-column names.

## Cross-domain reconciliation

Before a relationship can enter the CrossDomainSemanticGraph, validation reconciles:

1. **entity grain** — the real-world entity or event represented on each side;
2. **aggregation grain** — the level at which each measure can be combined without duplication;
3. **time zone and availability** — comparable instants and what was knowable at the relevant time;
4. **calendar and fiscal periods** — period definitions, cutoffs, partial periods, and mappings;
5. **currency** — currency identity, conversion source, rate type, and effective time where needed;
6. **units** — dimensions, scale, denominator, stock/flow behavior, and conversion compatibility;
7. **transformation and evidence** — explicit reproducible mapping and support state.

Failure or ambiguity limits, blocks, or requires confirmation. No arbitrary join or graph edge is
created merely to satisfy a user, Domain Experience, benchmark, or scenario request.

## Join safety

Before materializing an analytical view:

- verify key uniqueness and relationship cardinality;
- calculate match/orphan/duplicate coverage;
- identify measures that would multiply across a one-to-many or many-to-many join;
- aggregate or otherwise transform each measure to a valid grain before combination;
- preserve the join plan, evidence, mapping versions, filters, and row-count diagnostics;
- block unsafe direct aggregation of a one-side measure after a one-to-many join.

## Feature and relationship lineage

Lineage records exact derivation, binning, filtering, imputation, transformation, aggregation,
canonicalization, allocation, semantic redundancy, source versions, and temporal availability.
Derived fields retain their parents and cannot be treated as independent observed evidence.

Same-period persona, cluster, aggregate, or outcome-derived features cannot predict the outcomes
from which they were derived. Prediction-horizon checks use availability time, not file presence.

## Inference lifecycle

```text
infer → validate → confirm when ambiguous → persist as a new version
```

Statistical association, name similarity, or a Domain Experience catalog may propose a relationship;
none can independently establish it as supported truth.
