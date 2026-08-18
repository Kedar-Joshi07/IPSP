---
applyTo: "backend/**/{ingestion,profiling,semantics,relationships,capabilities}/**/*.py"
---
# Data & Semantic Instructions

- Do not infer from names alone. Combine statistical evidence, descriptions, relationships, lineage, and confirmations.
- Track physical dtype separately from semantic type.
- Model entity scope, measurement unit, temporal availability, sampling provenance, derived/lineage relationships, and confidence.
- Detect potential target leakage, post-outcome features, aggregate leakage, and join multiplication.
- Treat narrative/commentary embedded in workbooks as lower authority than raw records.
- Benchmark samples may be 500-row random extracts of much larger datasets; never infer full-population model sufficiency from sample size alone.
- Domain Experience activation uses versioned semantic evidence and compatibility; never branch on
  a domain name or physical source label in generic core.
- Metric requests resolve through the Metric & Formula Registry. Reconcile entity/grain/cardinality,
  time/calendar/fiscal, unit/currency/scale, transformation, and evidence before supporting a
  CrossDomainSemanticGraph relationship.
- No defensible relation means clarify, limit, or refuse—never invent a join or graph edge.
