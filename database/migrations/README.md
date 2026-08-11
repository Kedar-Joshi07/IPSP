# Database Migrations

This is the single canonical Alembic history root. Phase 1C establishes the no-op foundation
baseline. Phase 1D revision `20260811_02` adds only `roles`, `permissions`, `role_permissions`, and
`users`; it contains no production seed data or authentication/authorization behavior.

Run commands from the repository root. The Alembic environment reads the same validated
`IPSP_DATABASE__*` settings as the application; `alembic.ini` intentionally contains no duplicate
database URL.
