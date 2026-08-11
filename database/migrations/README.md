# Database Migrations

This is the single canonical Alembic history root. Phase 1C establishes a no-op foundation baseline;
business entity tables remain deferred to their owning implementation phases.

Run commands from the repository root. The Alembic environment reads the same validated
`IPSP_DATABASE__*` settings as the application; `alembic.ini` intentionally contains no duplicate
database URL.
