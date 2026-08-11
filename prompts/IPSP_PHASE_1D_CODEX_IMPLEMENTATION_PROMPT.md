# IPSP v1.0 — Phase 1D Codex Implementation Prompt
## User / Role / Permission Security-Schema Foundation

You are implementing the next reviewed work package in the existing IPSP repository.

**Repository:** `Kedar-Joshi07/IPSP`
**Required starting point:** commit `efb8423af8901d19689614d3cf635843e3da88d5` or an exact direct descendant containing no unreviewed Phase 1D work.

Current reviewed gate state:
- Phase 0: COMPLETE
- Phase 0.5: PASS
- Documentation Freeze: PASS
- Phase 1A: PASS
- Phase 1A.1: PASS
- Phase 1B: FINAL PASS
- Phase 1C: FINAL PASS
- Phase 1C.1: FINAL PASS
- Phase 1D: AUTHORIZED
- Application version remains `v0.1.0`

This task is **Phase 1D only**.

Do not begin Phase 1E authentication/session behavior or Phase 1F RBAC enforcement.

# 1. Governing security model

The frozen repository documentation is the authority.

The security model that Phase 1D must establish structurally is:

```text
User.role_id
    ↓
Role
    ↓
RolePermission
    ↓
Permission
```

This is the only authorization authority in IPSP.

Critical invariants:
1. V1.0 uses one role per user.
2. There is no persisted `is_admin` field.
3. No authorization shortcut may be introduced.
4. If a future API exposes an `is_admin` convenience value, it must be computed from resolved role/permissions only; Phase 1D does not implement such an API.
5. `username` is unique.
6. `email` is nullable.
7. Security timestamps have timezone-aware UTC semantics.
8. Database access remains synchronous SQLAlchemy 2.x.
9. `Session.query()` remains prohibited.
10. `database/migrations/` remains the single Alembic history.
11. Foreign-key enforcement remains mandatory.
12. Repositories own future data access, but Phase 1D does not need to invent repository/service layers before behavior exists.
13. Frontend remains HTML + CSS + Vanilla JavaScript.
14. Streamlit remains prohibited.

# 2. Required reading before editing

Read completely:
1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_PROJECT_STRUCTURE.md`
6. `docs/18_SECURITY_RBAC_SPEC.md`
7. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
8. `docs/23_ERROR_HANDLING_SPEC.md`
9. `docs/27_SQLITE_SCHEMA_SPEC.md`
10. `docs/29_TEST_STRATEGY.md`
11. `docs/30_ACCEPTANCE_CRITERIA.md`
12. `docs/31_IMPLEMENTATION_PROGRESS.md`
13. `docs/32_DECISION_LOG.md`
14. `docs/34_CODING_STANDARDS.md`
15. `docs/35_CONFIGURATION_SPEC.md`
16. `docs/37_SYSTEM_HEALTH_SPEC.md`
17. `docs/40_ANTI_CONTAMINATION.md`
18. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Then inspect:
- `backend/ipsp/database/models/base.py`
- `backend/ipsp/database/models/__init__.py`
- `backend/ipsp/database/engine.py`
- `backend/ipsp/database/session.py`
- `backend/ipsp/database/migrations.py`
- `database/migrations/env.py`
- `database/migrations/versions/20260811_01_phase1c_baseline.py`
- `tests/architecture/test_conformance.py`
- `tests/unit/test_database.py`
- `tests/integration/test_database_foundation.py`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `pyproject.toml`
- `requirements.lock`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Preserve unrelated user-owned/untracked prompt files.

# 3. Phase 1D objective

Implement the first real SQLite control-plane ORM schema for security identity and authorization structure.

Phase 1D must add exactly these production tables:

```text
roles
permissions
role_permissions
users
```

It must establish:
- canonical SQLAlchemy 2.x ORM models;
- exact foreign keys;
- exact uniqueness rules;
- user lifecycle/security-state columns required by the frozen specification;
- role-to-permission mapping as the sole authorization structure;
- timezone-aware UTC persistence semantics for security timestamps under SQLite;
- a new Alembic migration descending from the Phase 1C baseline;
- schema round-trip and constraint tests;
- architecture-conformance updates appropriate for the first legitimate ORM tables.

Phase 1D is schema only.

It does not authenticate anyone and does not authorize any request.

# 4. Explicitly out of scope

Do NOT implement:
- password hashing;
- `pwdlib`;
- Argon2id implementation;
- bcrypt;
- password pepper;
- login;
- logout;
- session token generation;
- user session validation;
- user session rotation;
- `user_sessions` table;
- `user_preferences` table;
- CSRF;
- cookies;
- lockout service logic;
- failed-login increment service logic;
- authentication routes;
- Admin routes/UI;
- bootstrap admin CLI;
- RBAC service;
- permission checking;
- `PermissionDeniedException` route behavior;
- user-management API;
- role-management API;
- generic BaseRepository;
- audit persistence;
- jobs schema;
- dataset permissions;
- projects/datasets;
- LLM configuration persistence;
- feature-flag persistence;
- outbound-policy persistence;
- ingestion;
- ML;
- simulation;
- Redis/Celery;
- async SQLAlchemy;
- automatic migration execution on app startup;
- production `Base.metadata.create_all()`.

Phase 1E will own authentication/session behavior.
Phase 1F will own RBAC authorization behavior.

# 5. Canonical ORM ownership

All ORM entities added in this phase must live under:

```text
backend/ipsp/database/models/
```

Preferred:
```text
backend/ipsp/database/models/security.py
```

There must be:
- one `User`;
- one `Role`;
- one `Permission`;
- one `RolePermission`;
- no duplicate security ORM classes elsewhere.

Use the existing canonical `Base`.

Use SQLAlchemy 2.x typed declarative syntax:

```python
Mapped[...]
mapped_column(...)
```

Do not use legacy declarative `Column(...)` style for new production models.

# 6. roles table

Required fields:

```text
id
name
description
```

Requirements:
- integer primary key;
- `name` non-null and unique;
- `description` may be nullable unless an existing frozen requirement explicitly makes it mandatory;
- no `is_admin`;
- no `is_system_admin`;
- no role-level Boolean that bypasses permissions;
- no JSON/comma-separated permission blob.

Do not seed production role rows in this phase. Tests may insert temporary Admin/User rows.

# 7. permissions table

Required fields:

```text
id
code
description
```

Requirements:
- integer primary key;
- `code` non-null and unique;
- description may be nullable;
- permission code is an opaque stable identifier such as `simulation.run`;
- no permission-level allow/admin Boolean.

Frozen examples include:
`simulation.run`, `simulation.export`, `dataset.view`, `dataset.upload`, `dataset.configure`, `dataset.assign`, `model.train`, `model.promote`, `llm.configure`, `internet.configure`, `user.manage`, `logs.view`, `system.configure`.

Do not silently invent an expanded production permission catalog.
Do not seed production permission rows in this phase.

# 8. role_permissions table

Required fields:

```text
role_id
permission_id
```

Use the pair as the composite primary key unless frozen schema says otherwise.

Requirements:
- FK `role_id -> roles.id`;
- FK `permission_id -> permissions.id`;
- duplicate mappings impossible;
- mapping rows are the sole structural source of role authorization;
- no allow/deny Boolean;
- no wildcard shortcut;
- no role hierarchy.

# 9. users table

Implement exactly the frozen minimum fields:

```text
id
username
display_name
email
password_hash
role_id
is_active
must_change_password
failed_login_count
locked_until
last_login_at
password_changed_at
created_at
created_by
updated_at
```

Rules:
- `id`: integer PK
- `username`: non-null, unique
- `display_name`: non-null
- `email`: nullable
- `password_hash`: non-null
- `role_id`: non-null FK to `roles.id`
- `is_active`: non-null, default true
- `must_change_password`: non-null, default true
- `failed_login_count`: non-null, default 0
- `locked_until`: nullable aware UTC
- `last_login_at`: nullable aware UTC
- `password_changed_at`: non-null aware UTC
- `created_at`: non-null aware UTC
- `created_by`: nullable self-FK to `users.id`
- `updated_at`: non-null aware UTC

There must be no persisted `is_admin`, `is_superuser`, `admin_flag`, `superuser`, `permission_level`, `access_level`, or equivalent bypass.

Email uniqueness is not frozen. Do not add an email uniqueness constraint unless a frozen spec explicitly requires it.

Add an intrinsic DB check:
```text
failed_login_count >= 0
```

Do not implement the service logic that changes this counter yet.

# 10. Timezone-aware UTC persistence

SQLite does not natively preserve timezone-aware datetime semantics in the same way as PostgreSQL.

Do not merely use `DateTime(timezone=True)` and assume SQLite round-trips tzinfo correctly.

Implement one reusable SQLAlchemy boundary, e.g. `UTCDateTime`, that guarantees:

```text
aware datetime input
    ↓
normalize to UTC
    ↓
persist
    ↓
read
    ↓
aware UTC datetime
```

Requirements:
- reject naive datetime values;
- normalize aware non-UTC offsets to UTC;
- return timezone-aware UTC datetimes;
- support nullable timestamps;
- remain compatible with Alembic;
- one implementation only.

A small `TypeDecorator` under database infrastructure ownership is appropriate.

# 11. Defaults

Preferred:
- `created_at`: UTC current timestamp default
- `updated_at`: UTC current timestamp default
- `password_changed_at`: UTC current timestamp default
- `is_active`: true
- `must_change_password`: true
- `failed_login_count`: 0

Do not create triggers for `updated_at`.
Future service/repository logic can update it explicitly.

Ensure ORM/migration defaults agree so `alembic check` is clean.

# 12. Relationships / foreign keys

Schema FKs must represent:

```text
User.role_id -> Role.id
User.created_by -> User.id
RolePermission.role_id -> Role.id
RolePermission.permission_id -> Permission.id
```

ORM relationships may be added if they remain simple and typed.

Avoid destructive cascades on users.
Do not implement authorization behavior in relationship properties.

# 13. Alembic migration

Create one new migration under the sole history.

It must:
- have `20260811_01` as direct ancestor;
- create exactly `roles`, `permissions`, `role_permissions`, `users`;
- create all required PK/FK/unique/check constraints;
- create no other domain table;
- contain no seed user/password/role/permission data;
- downgrade cleanly to Phase 1C baseline;
- re-upgrade cleanly.

Use existing deterministic naming convention.

After upgrade, `alembic check` must produce no unexpected operations.

# 14. Model metadata registration

`from ipsp.database.models import Base` must expose metadata containing exactly:

```text
permissions
role_permissions
roles
users
```

No second Base.

# 15. No production seeding

Do not insert:
- Admin user
- normal user
- default password/hash
- role rows
- permission rows
- role-permission rows

Temporary test rows are expected.

# 16. No password implementation

`password_hash` exists only because the frozen schema requires it.

Do not:
- hash/verify passwords;
- add pwdlib/Argon2;
- generate credentials;
- add password API schemas.

Tests should use unmistakable fake values like:
`TEST_HASH_NOT_A_REAL_PASSWORD`.

# 17. Schema tests

On isolated temp DB after `upgrade head`, verify:
- tables are exactly the four security tables plus `alembic_version`;
- no `user_sessions`;
- no `user_preferences`;
- no project/dataset/job/audit tables;
- users has exactly the frozen columns;
- no `is_admin` or equivalent bypass;
- username unique;
- email nullable;
- role name unique;
- permission code unique;
- role_permissions composite PK prevents duplicates;
- users.role_id FK enforced;
- users.created_by self-FK exists;
- role-permission FKs enforced;
- failed_login_count cannot be negative;
- non-nullability/defaults are present.

Use inspection and real insert failures.

# 18. ORM behavior tests

Using canonical session factory, prove:
- insert Role;
- insert Permission;
- insert RolePermission;
- insert User;
- query with SQLAlchemy 2.x `select()` / `Session.scalars()` / `Session.execute()`;
- explicitly join User -> Role -> RolePermission -> Permission;
- duplicate username fails;
- duplicate role name fails;
- duplicate permission code fails;
- duplicate mapping fails;
- nonexistent role FK fails;
- negative failed-login count fails.

Do not build an RBAC service to make these tests pass.

# 19. UTC tests

Using real temp SQLite:
1. UTC-aware input round-trips as aware UTC.
2. Aware `+05:30` input normalizes to UTC and returns UTC.
3. Naive datetime input is rejected.
4. Nullable timestamp fields accept None.
5. Default timestamps read back as aware UTC.
6. No security timestamp silently returns naive values.

# 20. Migration lifecycle

Using a fresh temp DB:

```text
20260811_01 baseline -> upgrade head
head -> downgrade 20260811_01
20260811_01 -> re-upgrade head
```

Verify:
- revision changes correctly;
- one script head remains;
- migration-state service reports at-head correctly;
- `alembic check` passes;
- downgrade removes four security tables;
- re-upgrade restores exactly them;
- readiness is ready only at Phase 1D head;
- a DB at Phase 1C baseline returns HTTP 503 + `SYS-MIGRATION-REQUIRED`.

Never touch developer default `database/ipsp.db`.

# 21. Update conformance guard

Phase 1C.1 has a temporary no-table guard. Replace it with a strict Phase 1D allowlist:

```text
roles
permissions
role_permissions
users
```

Conformance must fail if an extra ORM table appears.

Also verify:
- one DeclarativeBase
- only database/models ownership
- no persisted is_admin/admin bypass
- no user_sessions/user_preferences
- no auth/RBAC behavior
- no Session.query
- no AsyncSession
- no create_async_engine
- no aiosqlite
- no production create_all
- exactly one Alembic root
- no Streamlit
- no React/Vue/Angular
- no runtime CDN
- no JWT/python-jose
- no Redis/Celery
- no outbound HTTP/network implementation
- no benchmark contamination

# 22. Readiness

Do not redesign readiness.

Because Phase 1D becomes Alembic head:
- migrated Phase 1D DB -> HTTP 200
- Phase 1C-only DB -> HTTP 503 + `SYS-MIGRATION-REQUIRED`
- FK-disabled DB -> HTTP 503
- liveness remains HTTP 200

Do not expose security schema details through health.

# 23. Dependency policy

No new dependency should be necessary.

Do not add:
- pwdlib
- Argon2
- cryptography
- auth libraries
- JWT
- DB drivers

If no dependency changes:
- `pyproject.toml` unchanged
- `requirements.lock` unchanged
- do not create a clean lock-regeneration venv merely for this phase.

If a dependency is genuinely necessary, stop and report before adding it.

# 24. Privacy

Preserve Phase 1C.1 `hide_parameters=True`.

Do not log:
- real passwords
- secret values
- tokens
- complete user records

Use fake test data only.

# 25. Quality gates

Run:

```text
python -m compileall -q backend tests
pytest
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
```

Also run isolated migration smoke:

```text
alembic heads
alembic upgrade head
alembic current
alembic check
alembic downgrade 20260811_01
alembic upgrade head
```

Do not claim PASS unless actually run.

# 26. Documentation

Update:
- `database/migrations/README.md` if needed
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Record:
`Phase 1D — User / Role / Permission Security-Schema Foundation`

Document:
- four tables
- role-to-permission structural authority
- no persisted is_admin
- user minimum fields
- UTC handling
- migration revision
- constraint/test evidence
- no auth/session/RBAC behavior yet

Do not mark Phase 1 or v0.1.0 complete.

# 27. Git discipline

Before:
```text
git status --short
git rev-parse HEAD
```

After:
```text
git status --short
git diff --stat
git diff --check
```

Do not automatically commit/push.

Do not add DB files, WAL/SHM files, env files, venvs, logs, caches, or archives.

# 28. Acceptance gate

Phase 1D passes only if:
- exactly roles, permissions, role_permissions, users are added
- no Phase 1E+ table is added
- one canonical ORM class per entity
- typed SQLAlchemy 2.x mappings
- username unique
- email nullable
- role_id non-null FK
- created_by nullable self-FK
- password_hash non-null but no hashing implementation
- failed_login_count >= 0 enforced
- required lifecycle fields exist
- timestamps round-trip aware UTC
- naive timestamp writes fail
- role name unique
- permission code unique
- role-permission composite PK
- no is_admin/equivalent bypass
- no permission JSON/blob shortcut
- no role hierarchy
- no production seeds
- one new migration descends from 20260811_01
- upgrade/downgrade/re-upgrade passes
- alembic check passes
- one Alembic head
- readiness requires Phase 1D head
- Phase 1C privacy/FK protections remain intact
- no auth implementation
- no RBAC enforcement implementation
- no Streamlit/framework
- no new dependency
- full quality gates pass
- docs accurate

# 29. Mandatory final report

Return:

## A. Starting state
- starting SHA
- branch
- initial status

## B. Files created
List every file.

## C. Files modified
List every file.

## D. ORM schema
For each table show columns, PK, FK, uniqueness, nullability, defaults, checks.

## E. Authorization-structure proof
Confirm:
- `User.role_id -> Role -> RolePermission -> Permission`
- no persisted is_admin
- no equivalent bypass
- no authorization behavior yet

## F. UTC implementation
Explain normalization, naive rejection, round-trip evidence.

## G. Alembic
Report:
- new revision ID
- parent
- tables
- upgrade/current/head/check
- downgrade
- re-upgrade

## H. Constraint evidence
Report:
- username uniqueness
- role uniqueness
- permission-code uniqueness
- duplicate mapping rejection
- nonexistent role FK
- created_by FK
- negative failed-login rejection

## I. Readiness
Report:
- Phase 1D DB -> 200 ready
- Phase 1C baseline -> 503 migration required
- liveness -> 200

## J. Tests
Exact passed/failed/skipped/warnings.

## K. Quality gates
compileall, Ruff lint, Ruff format, mypy, pip check, diff check.

## L. Architecture/conformance
Report:
- ORM table allowlist
- duplicate ORM definitions
- persisted is_admin/admin shortcut
- user_sessions/user_preferences absence
- auth/RBAC absence
- Session.query
- AsyncSession
- async engine
- aiosqlite
- production create_all
- Alembic roots
- Streamlit
- React/Vue/Angular
- CDN
- JWT/python-jose
- Redis/Celery
- outbound HTTP
- benchmark contamination

## M. Dependency state
State whether pyproject/lock/dependencies changed.
If unchanged, confirm no clean lock venv was needed.

## N. Runtime artifacts
Report tracked/worktree DB/WAL/SHM/venv/cache/log artifacts.

## O. Git state
Final status and diff stat.

## P. Deviations / unresolved issues
If none: `None`

## Q. Gate result

End exactly with one:

`Phase 1D: PASS — ready for independent review before Phase 1E`

or

`Phase 1D: FAIL — Phase 1E blocked`

Do not begin Phase 1E.
