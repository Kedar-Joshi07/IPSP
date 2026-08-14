# Semantic Model Specification

## Status and authority

This planned contract is governed by the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md). A frozen Semantic Manifest contract is
not evidence that semantic inference or persistence is implemented in v0.1.0 or v0.1.1.

## Semantic object types

- Entity and identifier.
- Dimension, measure, measure family, and variant.
- Outcome/target candidate, controllable input, and non-controllable predictor/context.
- Time, availability time, business calendar, and fiscal period.
- Event, state, hierarchy, and relationship.
- Metric/derived measure reference and constraint/business rule.
- Attribution rule and prediction-horizon declaration.
- Sampling/provenance statement and sensitive-data classification.
- Feature lineage and semantic conflict.
- Domain Experience activation evidence and semantic-concept mapping.
- Cross-domain semantic node/relationship reference.
- Capability, scenario-intent, Trust/Evidence, and learning-eligibility facts.

## Column semantic metadata

Each source field can record generic metadata such as:

```text
source_name
canonical_name
physical_dtype
semantic_role
semantic_type
entity_scope
measurement_unit
currency_and_period_when_relevant
identifier_dimension_measure_flags
target_and_control_candidate_flags
derivation_and_lineage
availability_time
sensitivity_class
confidence
requires_confirmation
reason_and_evidence_summary
```

These are contract attributes, not required physical source columns.

## Dataset Semantic Manifest

Each confirmed dataset version produces an immutable, versioned Dataset Semantic Manifest capable
of representing:

- dataset and table-version references;
- entity scopes, identifiers, table grain, aggregation grain, and join constraints;
- field roles, semantic concepts, measures, dimensions, events, states, and outcomes;
- time zones, event/availability time, business calendars, fiscal periods, units, currencies, and
  conversions;
- relationships, hierarchies, CrossDomainSemanticGraph references, and feature lineage;
- missingness/sentinel meaning, intrinsic constraints, confirmed business rules, and sensitivity;
- metric IDs and Metric & Formula Registry version requirements;
- Domain Experience candidates, activation evidence, pack/manifest versions, and confirmation state;
- capability prerequisites and refusal-relevant limitations;
- ScenarioIntentManifest prerequisites and eligible semantic controls/constraints;
- Trust inputs and Evidence Profile provenance facts;
- observed-outcome identity and learning-eligibility facts;
- evidence, ambiguity, conflicts, confirmations, provenance, and supersession history.

The manifest references separate registry/graph contracts rather than duplicating their authority.

## Downstream contract boundary

The manifest must be capable of feeding:

1. the Metric & Formula Registry for validated semantic inputs and grain/time/unit behavior;
2. Domain Experience activation without requiring domain-specific physical columns;
3. CrossDomainSemanticGraph construction and reconciliation;
4. Capability Discovery and responsible refusal;
5. ScenarioIntentManifest validation and control/constraint eligibility;
6. separate Trust and Evidence Profile evaluation;
7. SimulationLearningStore and observed-outcome learning-eligibility gates.

Downstream services consume an exact manifest version. They do not reinterpret raw source names as
new semantic truth.

## Confidence and evidence

Raw LLM self-confidence is never final confidence. Semantic confidence combines deterministic
evidence, source descriptions, relationship consistency, prior confirmed organization knowledge,
structured proposal agreement, validation results, user confirmations, and conflict flags.

Evidence retains origin, method, version, timestamp, scope, and whether it is observed, derived,
configured, catalog-provided, assumed, externally sourced, synthetic, or proposed.

## Ambiguity and version lifecycle

```text
Ambiguity or conflict
  → targeted clarification
  → explicit confirmation or correction
  → validation
  → new Dataset Semantic Manifest version
```

User descriptions, observed behavior, related fields, curated catalogs, or uploaded narrative may
conflict. A conflict object blocks dependent capability when material; it is never silently
reconciled. A confirmation creates evidence for a new version rather than mutating a manifest that a
completed run already references.

## Schema-agnostic boundary

- Semantic concepts map to evidence-backed source fields; concepts never impose benchmark or domain
  field names on a dataset.
- A Domain Experience proposes vocabulary and prerequisites but cannot override confirmed dataset
  evidence or generic numerical truth.
- `Unknown` is not silently mapped to a negative label.
- Zero is not missing, and missing is not zero, without a confirmed semantic rule.
- Prediction, attribution, and causal-effect meanings remain distinct.
