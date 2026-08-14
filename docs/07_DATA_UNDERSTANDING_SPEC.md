# Data Understanding Specification

## Status and purpose

This is a planned deterministic contract under the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md). It does not claim that profiling or the
Data Intelligence Packet is implemented in v0.1.0 or v0.1.1.

Data Understanding converts structured/tabular inputs into reproducible evidence that can support
semantic interpretation and safe downstream decisions. It describes what was observed; it does not
silently decide business meaning, activate a domain, or enable a model from names alone.

## Data Intelligence Packet

For each dataset version, deterministic profiling produces a versioned packet capable of describing:

- source/table/sheet structure, size, checksum references, and parser provenance;
- row/column counts, duplicate evidence, sampling role, known source coverage, and observation
  maturity;
- candidate entities, identifiers, table grain, aggregation grain, and entity scope;
- candidate dimensions, measures, outcomes, predictors, controls, helper fields, events, and states;
- physical and logical types, missingness, blanks, sentinels, cardinality, and uniqueness;
- distributions, quantiles, ranges, gaps, outliers, and categorical frequencies where safe;
- time coverage, event/availability time, ordering, time zones, business calendars, and fiscal
  periods where evidence exists;
- units, currencies, scale, rate/ratio behavior, and conversion requirements where evidence exists;
- plan, actual, forecast, target, scenario, and variance candidates without assuming those concepts
  exist in every dataset;
- sensitivity and quasi-identifier evidence;
- relationship candidates, functional dependencies, hierarchy evidence, cardinality, and join
  multiplication risk;
- feature lineage, derivation, binning, aggregation, canonicalization, and redundant representations;
- provenance for every evidence item, including profiling algorithm/version and relevant parameters;
- evidence that may support future Domain Experience activation, without performing activation.

The packet contains evidence and uncertainty, not a fixed schema or a collection of mandatory
domain concepts.

## Dataset-level profiling

- Row and column counts by physical table.
- Table, sheet, file, and archive-member structure.
- Size, source type, and immutable source/version references.
- Date/time coverage and gaps where temporal fields are supported.
- Sampling/provenance metadata and known limitations.
- Duplicate-row and duplicate-entity evidence.
- Candidate grain, entity sets, keys, and cross-table identity evidence.
- Observation maturity, cutoff, and availability-time evidence.

## Column-level profiling

- Physical dtype and inferred logical dtype.
- Null, blank, sentinel, and semantic-missingness candidates.
- Cardinality, uniqueness, frequency, and safe example summaries.
- Numeric distributions, quantiles, ranges, and outlier evidence.
- Categorical frequencies with privacy-aware suppression where required.
- Date range, gaps, periodicity candidates, time zone, and calendar evidence.
- Candidate identifier, entity, dimension, measure, outcome, context, control, time, event, state,
  helper, or derived role.
- Unit, currency, scale, and period candidates.
- Sensitivity and quasi-identifier candidates.
- Availability relative to candidate prediction horizons.

## Relationship and lineage evidence

- Correlation and rank correlation where statistically and semantically meaningful.
- Mutual-information and categorical-association evidence where valid.
- Functional-dependency, key/foreign-key, identity, hierarchy, and cross-classification candidates.
- Cardinality, join coverage, orphan rates, and measure-duplication risk.
- Temporal direction, windows, selection rules, and maturity.
- Exact feature derivation and semantic redundancy.
- Entity, aggregation-grain, time, unit, and currency compatibility evidence for future cross-domain
  reconciliation.

Statistical association is not a semantic relationship, predictive guarantee, attribution rule, or
causal effect.

## Sampling and observation maturity

A random 500-row sample may support schema and example-semantic evaluation but cannot establish
full-population model sufficiency, true class balance, seasonality strength, rare-category
prevalence, complete relationship coverage, or stable Domain Experience activation.

Every packet records whether evidence is full, sampled, filtered, aggregated, time-windowed, or
otherwise incomplete and whether an outcome has had sufficient time to mature.

## Determinism and reproducibility

Packet reproduction requires the dataset version, source checksums, parser/profile versions,
non-secret configuration, sampling metadata, and deterministic parameters. Approximate or sampled
statistics are labeled with their method and coverage.

## Boundary rules

- No Domain Experience or benchmark may require a physical source-column name in generic profiling.
- Names are one evidence source; behavior, descriptions, relationships, lineage, and confirmations
  jointly carry greater authority.
- Zero and missing remain distinct unless confirmed semantics say otherwise.
- Negative monetary values are not universally invalid.
- Raw LLM output is not part of deterministic profiling evidence.
- Profiling evidence may propose semantics; ambiguity proceeds to clarification and confirmation.
