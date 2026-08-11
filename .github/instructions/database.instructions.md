---
applyTo: "backend/**/{database,repositories}/**/*.py"
---
# Database Instructions

- SQLite is the v1.0 control/knowledge database, not the mandatory store for millions of analytical rows.
- Use SQLAlchemy models/repositories and migrations; no scattered raw SQL.
- Preserve dataset versions, semantic versions, model versions, run lineage, audit metadata, and soft/archival states where specified.
- Keep repository interfaces portable enough for future PostgreSQL migration.
