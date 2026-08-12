# IPSP v1.0 — Phase 1F Codex Implementation Prompt
## RBAC Permission Enforcement, Core Permission Catalog & Privilege-Change Session Invalidation

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `9dafa7183bd8bf7925dbf9e6d8b8a32031fc52b8` or an exact direct descendant containing no unreviewed Phase 1F work.

Current reviewed gate state: Phase 0/0.5/1A/1A.1/1B/1C/1C.1/1D/1E/1E.1 all PASS. Phase 1F is AUTHORIZED. Application version remains `v0.1.0`.

This task is **Phase 1F only**. Do not begin Phase 1G observability/audit persistence, Phase 1H jobs, Phase 1I rich health, or general user/Admin UI work.

---

# 1. Frozen authorization authority

The sole authorization path is:

```text
User.role_id
    ↓
Role
    ↓
RolePermission
    ↓
Permission
```

Hard invariants:

- one role per user in v1.0;
- RolePermission rows are the sole grants;
- no persisted `is_admin` or equivalent;
- no runtime authorization rule based on `role.name == "Admin"`;
- no wildcard, permission level, access level, JSON permission blob, or role hierarchy;
- unknown/missing/inactive authorization state fails closed;
- server-side permission checks only;
- role/privilege changes invalidate affected sessions;
- no permission snapshots in cookies or `user_sessions`;
- sync SQLAlchemy 2.x only; repositories do not commit;
- no JWT, async SQLAlchemy, Redis/Celery, Streamlit, frontend framework, or network calls.

---

# 2. Read before editing

Read completely:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/00_SCOPE_FREEZE.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/40_ANTI_CONTAMINATION.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Inspect current source/tests, especially:

- `backend/ipsp/database/models/security.py`
- `backend/ipsp/repositories/auth.py`
- `backend/ipsp/auth/service.py`
- `backend/ipsp/api/dependencies/auth.py`
- `backend/ipsp/cli/admin.py`
- `backend/ipsp/config/providers.py`
- `backend/ipsp/errors/exceptions.py`
- `backend/ipsp/errors/handlers.py`
- `tests/architecture/test_conformance.py`
- `tests/integration/test_auth_api.py`
- `tests/integration/test_security_schema.py`
- `pyproject.toml`
- `requirements.lock`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Preserve user-owned/untracked prompt files.

---

# 3. Phase 1F objective

Implement:

1. typed core permission codes;
2. concrete permission/RBAC repositories;
3. `RBACService.has_permission(user_id, permission_code)`;
4. `RBACService.enforce_permission(user_id, permission_code)`;
5. domain-safe `PermissionDeniedException`;
6. reusable FastAPI permission dependency/factory;
7. fail-closed authorization;
8. role-change and role-permission-change session invalidation primitives;
9. idempotent core RBAC provisioning/synchronization;
10. explicit CLI for existing installations to synchronize RBAC;
11. fresh first-admin bootstrap integration so Admin becomes usable through mappings;
12. strong anti-bypass/security tests.

Do **not** implement general user/role-management REST APIs.

---

# 4. Out of scope

Do not implement `/api/v1/users` CRUD, role/permission management APIs, Admin UI, dataset ACL, project membership, user preferences, audit-event persistence, jobs, Admin system health, role hierarchy, multiple roles, ABAC, wildcard permissions, SSO/OAuth/OIDC/SAML/MFA, API keys, JWT, Redis/Celery, async SQLAlchemy, network calls, Streamlit, React/Vue/Angular, or new business tables.

---

# 5. No schema migration

Current schema already contains:

```text
users
roles
permissions
role_permissions
user_sessions
```

Phase 1F must add **no migration, table, column, or session permission snapshot**. Migration head remains `20260811_03`. `alembic check` must stay clean.

If a schema change appears necessary, stop and report it instead of adding one silently.

---

# 6. Core permission catalog

The frozen security spec lists these permission codes:

```text
simulation.run
simulation.export
dataset.view
dataset.upload
dataset.configure
dataset.assign
model.train
model.promote
llm.configure
internet.configure
user.manage
logs.view
system.configure
```

First verify no frozen document provides a contradictory required v1 foundation list. If this is the only core list, use **exactly these 13** as the Phase 1F initial core catalog. Do not invent extra codes.

Prefer a typed `StrEnum`, e.g. `CorePermission`.

Important:

- this enum protects first-party code from typos;
- `Permission.code` remains extensible string data;
- synchronization must preserve custom/plugin permissions;
- do not make the enum a permanent database allowlist;
- descriptions may remain `None` because canonical descriptions are not frozen;
- no `*`, `admin.all`, or hidden super-permission.

---

# 7. Initial provisioning policy

Ensure roles `Admin` and `User` exist.

**Admin:** explicitly map Admin to all 13 current core permissions through `role_permissions`. This is provisioning only; the role name has no runtime magic.

**User:** do not invent default grants. Ensure the role exists, but add no automatic core mappings. Preserve any mappings already present.

Synchronization must be additive/idempotent:

- ensure Admin/User roles;
- ensure 13 core Permission rows;
- ensure Admin mappings to all 13;
- preserve custom roles, permissions, and mappings;
- never prune.

---

# 8. Canonical code ownership

Prefer:

```text
backend/ipsp/auth/rbac.py
```

with concepts such as:

```text
CorePermission
RBACService
RBACCatalogService
```

Exact split may vary if a cleaner cohesive structure exists.

- `RBACService`: runtime authorization + narrow privilege mutation primitives.
- `RBACCatalogService`: idempotent initial role/permission/Admin-mapping provisioning.

No FastAPI types inside domain services.

---

# 9. Repositories

Add concrete repository ownership under `backend/ipsp/repositories/`, preferably `rbac.py`.

Do not add a generic BaseRepository.

Needed capabilities may include:

- Permission lookup/add;
- efficient `user_has_permission` query;
- list role permission codes;
- add/remove/replace role mappings;
- list user IDs by role;
- support catalog synchronization.

Reuse existing `UserRepository`, `RoleRepository`, `UserSessionRepository` rather than duplicating them.

Rules:

- receive canonical synchronous Session;
- SQLAlchemy 2.x `select()`/`execute()`/`scalars()`;
- no `Session.query()`;
- no commit/open transaction inside repositories.

---

# 10. Runtime permission resolution

`RBACService.has_permission(user_id, permission_code)` must query the **current database authority**.

Do not authorize from:

- role name;
- request/client role values;
- `request.state.role_name`;
- login-time permission snapshot;
- cookie/localStorage/sessionStorage;
- session permission list.

Effective authority is current persisted:

```text
users.id → users.role_id → role_permissions.role_id → permissions.id/code
```

Fail closed for:

- missing user;
- inactive user;
- missing role/mapping;
- unknown permission code.

Prefer one efficient EXISTS/join query. Do not cache permissions in Phase 1F.

---

# 11. Enforcement + error contract

Implement:

```text
RBACService.enforce_permission(user_id, permission_code)
```

Allowed => return normally. Denied => raise `PermissionDeniedException`.

Add `PermissionDeniedException` under existing domain error ownership. It must preserve IPSP safe error semantics and use:

```text
AUTHZ-PERMISSION_DENIED
Permission denied.
```

The existing handler should map it to HTTP 403.

Do not expose role membership, permission existence, SQL, token/session data, or internal details. Do not raise FastAPI `HTTPException` from the domain service.

---

# 12. FastAPI permission dependency

Add canonical API dependency ownership, e.g.:

```text
backend/ipsp/api/dependencies/rbac.py
```

Provide a reusable requirement such as conceptually:

```python
Depends(require_permission(CorePermission.USER_MANAGE))
```

It must:

1. depend on `require_authenticated_session`;
2. obtain canonical RBACService through app composition;
3. enforce using `principal.user_id`;
4. return the existing principal/context if allowed;
5. never authorize from `principal.role_name`;
6. preserve 401 for authentication failure;
7. produce safe 403 on authorization denial.

No SQL in dependency/routes. CSRF remains separate and composable.

---

# 13. Do not invent production endpoints

There is no Phase 1F business/Admin feature endpoint that needs to be invented now. Do not ship `/test-*` or artificial production routes.

Integration tests may attach temporary routes using the production dependency to prove enforcement.

Test both a protected GET and a POST that combines permission enforcement with existing CSRF.

---

# 14. Mandatory anti-bypass behavior

Tests must prove:

### Admin name without mapping
Role named `Admin`, required mapping removed:

```text
has_permission -> False
enforce_permission -> PermissionDeniedException
protected route -> 403
```

### Non-Admin role with mapping
A role such as `Analyst` with explicit mapping is allowed.

### Renamed role
Where practical, rename an authorized role while preserving its mapping; authorization remains based on role ID/mapping, not text label.

These behavioral tests are mandatory and stronger than string scans.

---

# 15. Fail-closed matrix

Test:

- unknown user -> deny;
- inactive user -> deny;
- unknown permission -> deny;
- valid user with no mapping -> deny;
- valid user with mapping -> allow;
- removed/deleted mapping -> deny;
- normal denial never becomes raw DB/500 error.

Client denial must not reveal whether the permission code exists.

---

# 16. Core RBAC synchronization service

Implement e.g.:

```text
RBACCatalogService.ensure_core_catalog()
```

It must:

1. ensure Admin/User roles;
2. ensure 13 core permissions;
3. ensure Admin mappings to all 13;
4. leave User without new automatic grants;
5. preserve custom roles/permissions/mappings;
6. delete nothing;
7. be idempotent;
8. optionally return a safe summary/count of changes.

Do not auto-run it at application startup or readiness.

---

# 17. Privilege-change session invalidation

The frozen security contract requires role/privilege changes to invalidate sessions.

Implement narrow internal service primitives, e.g.:

```text
assign_user_role(user_id, role_id, timestamp)
replace_role_permissions(role_id, permission_codes, timestamp)
```

No REST routes yet.

### User role change
If the role actually changes:

- persist role change;
- update user timestamp as appropriate;
- invalidate **all active sessions for that user** in the same application transaction;
- unrelated users unaffected;
- assigning same role is a no-op and should not invalidate.

### Role permission change
If effective role mappings change:

- persist mapping changes;
- invalidate active sessions for every user currently in that role;
- users in unrelated roles unaffected;
- identical mapping set is a no-op and should not invalidate.

Unknown roles/permissions fail safely.

---

# 18. Catalog sync is a privilege change when mappings are added

When core synchronization adds Admin mappings to an existing Phase 1E installation:

- invalidate active sessions for users currently assigned Admin;
- no-op second sync must not invalidate;
- User/custom-role sessions remain unaffected.

This ensures users reauthenticate after privilege expansion.

---

# 19. First-admin bootstrap integration

A fresh successful `ipsp-create-admin` must now leave the first Admin usable **through explicit RolePermission mappings**.

Requirements:

- database already at current migration head;
- no automatic migrations;
- still one-time when zero users;
- `getpass` password behavior unchanged;
- no default password;
- Admin/User roles ensured;
- exact 13 Permission rows ensured;
- Admin explicitly mapped to all 13;
- User receives no automatic core mappings;
- first user assigned Admin;
- no runtime Admin-name authorization shortcut.

Avoid partially mutating a refused second bootstrap where practical.

---

# 20. Existing-installation CLI

Add an explicit local command for databases that already have users, preferably:

```text
ipsp-sync-rbac
```

Suggested ownership:

```text
backend/ipsp/cli/rbac.py
```

Requirements:

- require current migration head;
- do not run migrations;
- run idempotent core catalog synchronization;
- users may already exist;
- print only safe counts/summary;
- no password/token/session output;
- repeated run safe/no-op;
- nonzero safe failure.

Adding a `[project.scripts]` entrypoint is allowed. If that is the only `pyproject.toml` change, dependency lock remains unchanged.

---

# 21. Extensibility regression

Before sync create test-only custom data:

```text
role: CustomRole
permission: plugin.example
mapping: CustomRole -> plugin.example
```

After sync prove all custom data still exists and core/Admin data was added.

Do not add `plugin.example` to production core constants.

---

# 22. Client authority prohibition

Do not add permission lists or authority to:

- cookies;
- localStorage/sessionStorage;
- URL values;
- JWT claims;
- `user_sessions`;
- hidden form values.

Keep `/api/v1/auth/me` as identity/session context. Do not add a permission list there in Phase 1F unless a frozen contract explicitly requires it.

---

# 23. Authentication interaction

Preserve all Phase 1E/1E.1 behavior.

Protected-route tests:

```text
unauthenticated          -> 401
authenticated+unauthorized -> 403
authenticated+authorized   -> success
disabled/expired session   -> 401
```

Permission enforcement occurs after authentication.

---

# 24. CSRF + RBAC composition

Temporary test POST route requiring both permission and CSRF must prove:

- valid session + permission + valid CSRF -> success;
- valid session + permission + invalid/missing CSRF -> `AUTHZ-CSRF_INVALID` 403;
- valid session + valid CSRF + missing permission -> `AUTHZ-PERMISSION_DENIED` 403;
- unauthenticated -> 401.

Do not merge CSRF into RBACService.

---

# 25. Privilege invalidation integration tests

Use real sessions.

### Role assignment
- user has multiple active sessions;
- change role via Phase 1F internal primitive;
- all that user's sessions invalidated;
- unrelated user's session survives;
- same-role no-op does not invalidate.

### Role mapping
- two users share role and have active sessions;
- third user in another role has active session;
- change shared role mappings;
- both shared-role sessions invalidated;
- unrelated-role session survives;
- identical mapping no-op does not invalidate.

---

# 26. Runtime freshness test

Prove permissions are not captured at login:

1. login user;
2. mapping exists -> allow;
3. remove mapping through Phase 1F service -> sessions invalidated;
4. fresh login -> deny;
5. re-add mapping -> affected sessions invalidated;
6. fresh login -> allow.

---

# 27. PermissionDeniedException API test

Prove:

```text
PermissionDeniedException
  -> existing IPSP handler
  -> HTTP 403
  -> AUTHZ-PERMISSION_DENIED
  -> safe generic message + trace ID
```

Response must not reveal role name, permission existence, SQL, bearer/session token, or password information.

---

# 28. Application composition

Extend `FoundationServices` explicitly with canonical RBAC service(s), e.g.:

```text
rbac_service
rbac_catalog_service
```

No global singleton, no DB work at import, no automatic RBAC provisioning on startup, no network calls.

Keep AuthService focused on authentication/session behavior.

---

# 29. Architecture/conformance evolution

Phase 1E currently prohibits `RBACService`, `has_permission`, `enforce_permission`; these are now legitimate. Evolve, do not weaken, conformance tests.

Phase 1F conformance must verify:

- RBAC service only under auth/domain ownership;
- permission DB access only in repositories;
- permission dependency only under API dependencies;
- no permission SQL in routes;
- no runtime role-name shortcut;
- no persisted `is_admin`/`is_superuser`/access-level bypass;
- no wildcard grant behavior;
- no permission snapshot in sessions;
- exact five ORM tables unchanged;
- one DeclarativeBase, one Alembic root;
- no new migration;
- no Session.query/AsyncSession/create_async_engine/aiosqlite/create_all;
- no JWT/python-jose/PyJWT;
- no bcrypt/passlib;
- no Redis/Celery/network clients;
- no Streamlit/React/Vue/Angular/runtime CDN;
- no benchmark contamination.

Behavioral tests must prove Admin has no magic bypass.

---

# 30. Dependencies and lock

No new dependency should be necessary.

- do not add packages;
- `requirements.lock` unchanged;
- do not regenerate lock;
- do not create clean dependency-resolution virtual environments.

`pyproject.toml` may change only for the `ipsp-sync-rbac` console entrypoint.

If a new dependency appears necessary, stop and report why.

---

# 31. Migration/readiness state

Migration chain remains:

```text
20260811_01 -> 20260811_02 -> 20260811_03
```

Run isolated:

```text
alembic heads
alembic current
alembic check
```

Readiness should not depend on RBAC catalog presence. Missing catalog => permission checks deny, not process unready. Do not auto-provision at startup/readiness.

---

# 32. Mandatory tests — catalog

After sync:

- the 13 core codes exist;
- Admin has all 13 explicit mappings;
- User receives no new automatic core mapping;
- custom roles/permissions/mappings survive;
- second sync no-op;
- no-op sync does not invalidate sessions;
- sync that adds Admin mappings invalidates existing Admin sessions only.

Do not assert that the permission table can contain only these 13 forever.

---

# 33. Mandatory authorization matrix

Test:

```text
authenticated + mapped permission       -> allow
authenticated + no mapping              -> 403
authenticated + unknown permission      -> 403
unauthenticated                          -> 401
inactive/disabled                        -> 401 via auth
role named Admin + mapping removed       -> 403
non-Admin role + explicit mapping        -> allow
renamed role + mapping retained          -> allow
```

---

# 34. Repository/service boundaries

Tests/source checks must prove:

- modern SQLAlchemy only;
- repositories do not commit;
- service owns session/transaction scopes;
- no SQL in routes;
- dependency calls service;
- no generic BaseRepository introduced.

Use real SQLite in integration tests.

---

# 35. Bootstrap/CLI tests

Fresh DB at head + create-admin should yield:

```text
Admin/User roles
13 core permissions
13 Admin mappings
0 automatic User mappings
first Admin user
```

Existing DB with users + `ipsp-sync-rbac` should ensure catalog without deleting users/custom data.

Test repeated sync, safe summary, no secrets, and second create-admin refusal.

---

# 36. Privacy/logging

Do not log bearer session tokens, CSRF tokens, passwords, password hashes, or token hashes. Permission codes are non-secret, but do not build verbose authorization logging; Phase 1G owns durable audit.

Existing redaction tests must remain green.

---

# 37. Quality gates

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

Also run isolated:

```text
alembic heads
alembic check
```

Do not claim PASS unless actually run.

---

# 38. Documentation

Update `docs/31_IMPLEMENTATION_PROGRESS.md` and CLI/local setup docs where needed.

Record:

```text
Phase 1F — RBAC Permission Enforcement
```

Document:

- sole authority path;
- exact initial 13 core codes;
- explicit Admin mappings;
- no runtime Admin shortcut;
- User fail-closed default;
- RBAC service/dependency;
- PermissionDeniedException;
- privilege-change session invalidation;
- `ipsp-sync-rbac`;
- first-admin integration;
- no schema migration/dependency change;
- test/quality evidence.

Do not mark general user management, dataset ACL, audit logging, Phase 1, or v0.1.0 complete. Phase 1G remains next.

---

# 39. Git discipline

Before/after:

```text
git status --short
git rev-parse HEAD
git diff --stat
git diff --check
```

Do not auto commit/push. Do not track DB/WAL/SHM, `.env`, token/password dumps, venvs, caches, logs, or archives.

---

# 40. Phase 1F acceptance gate

PASS only if:

- RolePermission path is sole runtime authority;
- no `is_admin`/Admin-name/wildcard shortcut;
- unknown permission fails closed;
- exact 13 initial core codes only;
- Admin explicitly mapped to all 13;
- User gets no automatic core grants;
- sync additive/idempotent/custom-data preserving;
- has/enforce permission implemented;
- safe PermissionDeniedException -> 403;
- reusable permission dependency implemented;
- Admin without mapping denied;
- non-Admin with mapping allowed;
- privilege changes invalidate correct sessions;
- no-op changes do not invalidate;
- fresh create-admin ensures RBAC;
- existing-install sync CLI works;
- five-table ORM allowlist unchanged;
- migration head stays `20260811_03`;
- no new dependency;
- no async/JWT/bcrypt/passlib/Redis/Celery/network/Streamlit/framework drift;
- all tests and quality gates pass.

---

# 41. Mandatory Codex final report

Return all sections:

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Core permission catalog
Exact 13 codes, representation, extensibility, no invented codes.

## E. Provisioning policy
Admin mappings, User default, idempotency, custom-data preservation.

## F. RBAC repository architecture
Classes/methods, SQLAlchemy patterns, no commit ownership.

## G. RBACService
`has_permission`, `enforce_permission`, fail-closed behavior, no role-name shortcut/caching.

## H. PermissionDeniedException
Ownership, error code, HTTP 403, safe response.

## I. API dependency
Auth composition, service call, test-only route evidence, CSRF composition.

## J. Anti-bypass evidence
Admin without mapping deny; non-Admin mapped allow; renamed mapped role allow; unknown permission deny.

## K. Privilege-change invalidation
User role change, role mapping change, affected/unrelated/no-op behavior.

## L. Core catalog synchronization
Roles/permissions/Admin mappings/User untouched/custom preserved/idempotent/session invalidation.

## M. Bootstrap / CLI
Fresh create-admin integration, `ipsp-sync-rbac`, existing users, migration-head requirement, safe output.

## N. Schema/migration state
ORM table allowlist, Alembic head, no migration, `alembic check`.

## O. Dependency state
pyproject dependency changes, requirements.lock, console-script-only change, no clean venv.

## P. Authentication regression status
Phase 1E/1E.1 login/session/CSRF/lockout/password/leak tests remain green.

## Q. Tests
Exact passed/failed/skipped/warnings.

## R. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, diff check.

## S. Architecture/conformance
Persisted admin bypass, role-name shortcut, wildcard/access-level bypass, permission snapshot, duplicate ORM ownership, legacy/async DB, create_all, JWT, bcrypt/passlib, Redis/Celery, HTTP, Streamlit/framework/CDN, benchmark contamination.

## T. Runtime artifacts
Tracked/worktree DB/WAL/SHM, token/password dumps, venvs, caches, logs.

## U. Git state
Final status + diff stat.

## V. Deviations / unresolved issues
If none: `None`

## W. Gate result

End exactly with one:

`Phase 1F: PASS — ready for independent review before Phase 1G`

or

`Phase 1F: FAIL — Phase 1G blocked`

Do not begin Phase 1G.
