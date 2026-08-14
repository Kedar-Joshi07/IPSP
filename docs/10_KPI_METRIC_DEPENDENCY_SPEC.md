# KPI & Metric Dependency Specification

## Status within F-002

This specification defines the dependency-discovery, validation, and evaluation subset of the
broader [Metric & Formula Registry Specification](46_METRIC_FORMULA_REGISTRY_SPEC.md). Its useful
predecessor logic is preserved, but it is not the identity, versioning, precedence, or numerical
authority for the complete registry.

## Goal

Discover, validate, and explain useful metric relationships without inventing business definitions
or imposing physical source-column names.

## Proposal sources

- Confirmed organization definitions and configuration.
- Deterministic arithmetic identities supported by observed rows.
- Confirmed semantic and relationship contracts.
- Curated Domain Experience metric requests.
- Explicit user assumptions, labeled as assumptions.
- Optional structured LLM proposals, never accepted without deterministic/schema validation.

Proposal source does not determine authority. Registry precedence, evidence, conflict, and version
rules remain mandatory.

## Formula and dependency validation

- The formula parses into the registry's safe representation using approved operators/functions.
- Every semantic input and upstream metric resolves to an exact version.
- Required grain and aggregation behavior are compatible.
- Time, calendar, fiscal-period, stock/flow, and window semantics are explicit.
- Denominator meaning and rate/ratio behavior are compatible.
- Division and null behavior are safe and declared.
- Units, currencies, scale, and conversions are compatible and versioned.
- Required filters, states, and maturity rules are explicit.
- The formula matches observed stored derived values where applicable, with tolerance documented.
- Dependency cycles and unsafe one-to-many aggregation are rejected.

## Qualified measures

A metric may qualify a measure by confirmed state, time, cohort, entity, maturity, or policy. The
qualification is part of the versioned definition and lineage; it is not inferred from one
benchmark or silently embedded in UI logic.

## Metric dependency graph

The dependency graph records upstream metric IDs/versions, semantic inputs, transformations,
filters, aggregation, grain, time, unit/currency behavior, validation evidence, and output metric.
It supports deterministic evaluation order, cycle detection, charts, scenarios, explanations,
exports, and reproducibility.

The graph is a representation inside the Metric & Formula Registry. Domain Experience Packs may
request metric IDs, but the generic registry and compute boundary own formula validation and
numerical evaluation.
