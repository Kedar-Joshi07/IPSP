# Database Migrations

This is the single canonical Alembic history root. Phase 1C establishes the no-op foundation
baseline. Phase 1D revision `20260811_02` adds only `roles`, `permissions`, `role_permissions`, and
`users`; it contains no production seed data or authentication/authorization behavior.

Phase 1E revision `20260811_03` directly follows `20260811_02` and adds only `user_sessions`. The
table stores SHA-256 session and CSRF token hashes, a non-secret correlation ID, its user foreign key,
and UTC lifecycle timestamps. It never stores raw cookie values, JWTs, refresh tokens, permission
snapshots, or admin snapshots, and the migration contains no seed data. Downgrading to
`20260811_02` removes only `user_sessions`.

Phase 1G revision `20260812_04` directly follows `20260811_03` and adds only `audit_events` for
selected durable audit/security envelopes. It stores historical scalar identity/correlation fields,
sanitized deterministic JSON metadata, and no raw credentials, bodies, headers, session tokens, or
future-domain foreign keys. Downgrading to `20260811_03` removes only `audit_events`; the five prior
security tables remain intact.

Run commands from the repository root. The Alembic environment reads the same validated
`IPSP_DATABASE__*` settings as the application; `alembic.ini` intentionally contains no duplicate
database URL.
