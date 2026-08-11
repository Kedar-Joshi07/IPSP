# Data Understanding Specification

## Purpose
Convert raw structured uploads into deterministic evidence that can support semantic interpretation and safe downstream modelling.

## Required profiling outputs

### Dataset
- Row/column counts
- Table/sheet/file structure
- Size and source type
- Date/time coverage
- Sampling/provenance metadata
- Duplicate rows
- Candidate grain
- Candidate entity set

### Column
- Physical dtype and inferred logical dtype
- Null/blank/sentinel counts
- Cardinality and uniqueness
- Example values
- Numeric distribution/quantiles/outliers
- Categorical frequencies
- Date range/gaps
- Candidate identifier/dimension/measure/time/helper/target/control role
- Unit/currency candidate
- Sensitive/quasi-identifier candidate

### Relationships
- Correlation/Spearman where meaningful
- Mutual information
- Functional dependency candidates
- Cramér's V/chi-square for categorical relationships
- Key/foreign-key candidates
- Cardinality/join multiplication risk
- Temporal ordering
- Feature lineage and redundant representations
- Hierarchies and cross-classifications

## Sampling awareness
A random 500-row sample may show schema and example semantics but cannot establish full-population model sufficiency, true class balance, seasonality strength, or rare-category prevalence.

## Never rely on names alone
Names are one evidence source. Statistical/data evidence, descriptions, related columns, temporal lineage, and user confirmation have higher combined authority.
