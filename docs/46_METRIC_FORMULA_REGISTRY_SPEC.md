# Metric & Formula Registry Specification

## Status and authority

**F-002 contract:** FROZEN

**Runtime implementation:** NOT IMPLEMENTED

**Owning target milestone:** v0.5.0 — Metric & Formula Registry + Domain Experience Foundation

This specification defines the provider-neutral contract for metric identity, formula truth,
validation, lineage, and deterministic evaluation. It is subordinate to the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and does not authorize v0.2.0 or create
runtime tables, APIs, dependencies, or calculation services.

## Governing boundary

Domain Experience Packs and organization catalogs may request semantic metric IDs. The Metric &
Formula Registry owns versioned numerical definitions and their validation. A generic compute
service evaluates accepted definitions against an exact Dataset Semantic Manifest and analytical
data version.

```text
Domain Experience or organization request
  → semantic metric ID
  → registry definition/version resolution
  → manifest/input/grain validation
  → generic deterministic evaluation
  → value + complete lineage
```

**Domain Pack does not equal Formula Engine.** A domain request, UI label, benchmark narrative, or
LLM proposal never becomes numerical truth by itself.

## Metric definition identity and versioning

Each conceptual definition includes:

| Field group | Required meaning |
|---|---|
| Identity | Stable metric ID, definition version, human label, description, and semantic concept |
| Compatibility | Contract/schema version and compatible registry/Domain Experience versions |
| Inputs | Semantic concept IDs and/or upstream metric IDs with exact versions |
| Formula | Safe typed representation, approved operations, constants with units, and qualifications |
| Aggregation | Additivity, aggregation function, required grain, grouping, allocation, and deduplication rules |
| Time | Event/as-of time, window, period, calendar/fiscal semantics, lag, stock/flow behavior, and maturity |
| Units | Input/output dimensions, scale, currency, rate/ratio denominator, and conversion references |
| Missingness | Null, sentinel, incomplete-period, denominator-zero, and safe-division behavior |
| Validation | Tests, tolerances, observed-value comparison, invariants, and evidence |
| Lineage | Sources, transformations, definition dependencies, provenance, and confirmation references |

Definitions are immutable once referenced by an accepted result. A correction, organization
override, formula change, semantic change, or compatibility change creates a new version and records
which definition it supersedes. Version identifiers are contract versions, not application releases.

Exact persistence columns and lifecycle-status enums are deferred to F2-G and the owning milestone.

## Semantic inputs and source mapping

Definitions reference semantic concepts, metric IDs, and grain/time/unit requirements. They do not
require benchmark or domain-specific physical source-column names. Each dataset's exact source-field
mapping belongs to a versioned Dataset Semantic Manifest and must pass compatibility validation.

An input contract identifies:

- semantic concept or upstream metric identity/version;
- entity scope and required grain;
- measure/dimension/state role;
- time, maturity, availability, calendar, and fiscal requirements;
- unit, currency, scale, and denominator requirements;
- null/sentinel and qualification behavior;
- evidence and confirmation requirements.

Missing or ambiguous prerequisites limit, block, or request clarification; the registry does not
guess a mapping to make a metric computable.

## Formula representation and safety

Formula definitions use a typed, schema-validated representation such as a constrained expression
tree. The implementation contract must:

- allowlist operators, aggregation functions, window functions, conversions, and safe helpers;
- distinguish metric references, semantic inputs, typed constants, filters, and conditions;
- forbid arbitrary Python, SQL, shell, template, or LLM-generated executable code;
- type-check numeric, Boolean, categorical, temporal, unit, and currency operations;
- make qualifications and denominators explicit;
- produce a canonical representation/hash for reproducibility.

An implementation syntax will be frozen before runtime work. This document does not select one.

## Dependency graph

The registry maintains a versioned directed dependency graph whose nodes are metric definitions and
semantic inputs. It supports:

- upstream/downstream traversal;
- deterministic evaluation ordering;
- cycle detection and rejection;
- impact analysis when a definition or input version changes;
- shared evaluation for analysis, charts, scenarios, explanations, and exports;
- exact dependency snapshots for re-run and reproduce.

The [KPI & Metric Dependency Specification](10_KPI_METRIC_DEPENDENCY_SPEC.md) governs this
dependency-discovery and evaluation subset.

## Aggregation and grain semantics

Each definition declares whether a measure is additive, semi-additive, non-additive, ratio/rate,
stock, flow, distinct-count-like, or otherwise constrained. Validation covers:

- source and output grain;
- grouping dimensions and roll-up behavior;
- required pre-aggregation and deduplication;
- allocation rules and their evidence;
- one-to-one, one-to-many, and many-to-many relationship effects;
- whether averaging, summing, recomputing, last-value, or another operation is valid.

A one-side measure is never directly aggregated after a one-to-many join without a validated safe
transformation to the required grain.

## Time semantics

Definitions make explicit:

- event time versus processing/availability/as-of time;
- observation window, comparison window, lag, and horizon;
- calendar, business calendar, fiscal period, and time zone;
- partial-period, incomplete-period, maturity, and restatement behavior;
- point-in-time stock versus period flow behavior;
- plan, actual, forecast, target, scenario, or variance comparison where applicable.

Time alignment never assumes two similarly named periods are comparable.

## Units, currencies, and scale

Definitions declare input/output units, dimensional compatibility, scale, currency, and rate/ratio
denominators. Currency conversion requires an explicit versioned source, rate type, effective time,
and direction. A monetary measure is not presumed non-negative.

Incompatible units/currencies block evaluation unless an approved conversion or reconciliation
contract exists.

## Null, sentinel, and safe-division behavior

Every definition declares behavior for missing, unknown, not-applicable, suppressed, immature, and
sentinel inputs. Zero and missing are distinct unless confirmed semantics establish a rule.

Ratios declare denominator meaning and zero/null behavior. Silent infinity, coercion, imputation,
or substitution is prohibited. Partial results expose coverage and limitation reasons.

## Validation contract

Before a definition is eligible for operational use, validation covers:

- schema and type validity;
- semantic prerequisite and confirmation state;
- dependency resolution and acyclicity;
- grain/cardinality and aggregation safety;
- time/calendar/fiscal and maturity compatibility;
- unit/currency/scale compatibility;
- null/sentinel/safe-division behavior;
- deterministic examples or property/invariant tests;
- comparison to observed stored values where applicable, with explicit tolerances;
- provenance, policy, and reproducibility completeness.

Validation failures retain reason codes and evidence. An LLM may propose a definition but cannot
approve it or waive deterministic validation.

## Lineage and provenance

Each computed value retains:

- metric ID and exact definition version;
- Dataset Semantic Manifest and dataset/table versions;
- upstream metric versions and dependency-graph snapshot/hash;
- source mappings, transformations, filters, aggregation, and conversions;
- organization configuration, Domain Experience request, confirmation, or user-assumption source;
- validation result/version, compute implementation version, and non-secret configuration hash;
- coverage, warnings, and evidence references.

## Catalog precedence and organization overrides

Metric requests and candidate definitions follow the frozen precedence:

1. organization-configured and governed definitions;
2. observed or confirmed dataset values and definitions;
3. curated Domain Experience Pack requests/definitions;
4. explicit custom user assumptions.

Higher precedence does not bypass intrinsic validity, semantic compatibility, provenance, licensing,
or validation. An organization override creates a versioned governed definition; it does not mutate
a curated definition or rewrite historical results.

## Conflict behavior

A conflict exists when eligible sources disagree about formula, semantic inputs, aggregation, grain,
time, currency/unit behavior, qualification, or null rules. The registry:

1. records all candidates and evidence;
2. applies precedence only where policy permits;
3. requests confirmation when material ambiguity remains;
4. blocks dependent capabilities while unresolved;
5. persists the accepted resolution as a new version;
6. retains superseded definitions for historical reproduction.

No silent last-write-wins rule is permitted.

## Reproducibility

Reproduction references the dataset and table versions, Dataset Semantic Manifest, metric
definition/dependency versions, Domain Experience/configuration versions, source mappings,
conversion sources, validation evidence, compute implementation, and non-secret configuration.

Re-run may select a newer eligible definition only when clearly distinguished from reproduce.

## Deferred implementation detail

F2-C freezes semantics and ownership only. Exact database tables, API resources, expression syntax,
cache strategy, compute engine, lifecycle enums, and migration plan require later contract freezes.
No runtime capability or dependency is introduced here.
