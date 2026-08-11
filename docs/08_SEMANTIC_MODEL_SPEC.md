# Semantic Model Specification

## Semantic object types

- Entity
- Identifier
- Dimension
- Measure
- Measure family / variant
- Target candidate
- Controllable input
- Non-controllable predictor/context
- Time / business calendar
- Event
- State
- Hierarchy
- Relationship
- KPI / derived measure
- Constraint / business rule
- Attribution rule
- Sampling/provenance statement
- Sensitive-data classification
- Feature lineage
- Prediction-horizon availability

## Column semantic metadata
Each column should be able to record:

```text
source_name
canonical_name
physical_dtype
semantic_role
semantic_type
entity_scope
measurement_unit
currency/period if relevant
is_identifier / is_dimension / is_measure
is_target_candidate / is_controllable
is_derived
lineage_parents
availability_time
sensitivity_class
confidence
requires_confirmation
reason/evidence summary
```

## Confidence
Do not use raw LLM self-confidence as final confidence. Combine deterministic evidence, descriptions, relationship consistency, user-confirmed history, LLM agreement/consistency, and conflict flags.

## Semantic conflicts
When user description, column behavior, related fields, or uploaded narrative conflict, create a conflict object and ask a targeted question. Never silently reconcile.

## Manifest
Every confirmed dataset version produces a versioned Dataset Semantic Manifest used as the contract for downstream capability/model/simulation services.
