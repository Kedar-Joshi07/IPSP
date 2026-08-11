# KPI & Metric Dependency Specification

## Goal
Discover useful formulas without inventing business definitions.

## Formula proposal sources
- User-provided definitions
- Deterministic arithmetic identities discovered from rows
- Established semantic relationships
- Optional LLM proposal

## Validation
- Formula parses against approved fields/functions.
- Denominator semantics are compatible.
- Division is safe.
- Units/currencies are compatible.
- Required filters/states are explicit.
- Formula matches observed stored derived values where applicable.

## Qualified measures
Support measures such as `revenue where status = complete`, `mature cohort fulfilment`, or other state/time-qualified values.

## Metric dependency graph
Persist upstream measures, transformation, filters, unit, and output measure. This graph is reusable by charts, deterministic scenarios, explanations, and exports.
