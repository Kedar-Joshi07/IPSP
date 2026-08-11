# Relationships, Hierarchy & Lineage

## Relationship categories

### Structural
One-to-one, one-to-many, many-to-many.

### Identity
Exact join, normalized join, derived/canonical identity.

### Temporal
Same-entity plus direction/window/selection rule; supports attribution semantics.

### Ordered journey
Stage metric graph; may or may not be monotonic depending on measurement units and re-entry.

### Lifecycle/state
Operational progression plus exception states.

### Measure dependency
Algebraic/derived KPI relationships.

### Plan vs actual
Planned/target measure paired with actual measure.

### Commercial flow
Related business movement such as upstream/downstream measures.

### Hierarchy
Strict functional hierarchy, soft hierarchy, cross-classification.

## Feature lineage
Track exact derivation, binning, transformation, aggregation, canonicalization, and semantic redundancy.

## Join safety
Before materializing a multi-table analytical view, compute cardinality and identify measures that would duplicate after a join. Unsafe aggregation must be blocked or explicitly transformed to the correct grain.
