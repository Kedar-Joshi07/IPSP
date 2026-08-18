---
applyTo: "backend/**/{database,repositories}/**/*.py"
---
# Database Instructions

- SQLite is the v1.0 control/knowledge database, not the mandatory store for millions of analytical rows.
- Use SQLAlchemy models/repositories and migrations; no scattered raw SQL.
- Preserve dataset versions, semantic versions, model versions, run lineage, audit metadata, and soft/archival states where specified.
- Future registry, Domain Experience, graph, evidence, consent, license, learning, and outcome records
  must preserve exact versions/provenance and their control-plane authority; they must not turn
  simulated or synthetic values into ordinary observed rows.
- Keep repository interfaces portable enough for future PostgreSQL migration.
