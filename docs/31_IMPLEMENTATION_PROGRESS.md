# Implementation Progress

Specification baseline: **IPSP v1.0 frozen**  
Application implementation: **Phase 1F RBAC permission enforcement complete. Phase 1G blocked pending independent review.**

| Milestone | Target app version | Status | Gate |
|---|---|---|---|
| Specification & plan generation | — | PHASE 0 COMPLETE | 40+ numbered specs + implementation plan ready |
| Architecture reconciliation | — | **PHASE 0.5 PASS** | 24 audit/completeness items resolved; all 20 gates verified |
| Foundation/security/repo skeleton | v0.1.0 | **PHASE 1 IN PROGRESS (1F PASS)** | Phase 1F current-database permission enforcement, explicit core provisioning, and privilege-change session invalidation passed; Phase 1G not started |
| Ingestion/storage/provenance | v0.2.0 | NOT STARTED | Supported uploads + versioning tests |
| Data understanding/relationships | v0.3.0 | NOT STARTED | Benchmark semantic profiles |
| Semantic manifest/clarification | v0.4.0 | NOT STARTED | Versioned manifest + conflict workflow |
| Capability/model validation | v0.5.0 | NOT STARTED | Baseline/model gates |
| Simulation/trust/history | v0.6.0 | NOT STARTED | Reproducible runs + trust gate |
| Dynamic frontend/light theme | v0.7.0 | NOT STARTED | UI acceptance |
| Local LLM | v0.8.0 | NOT STARTED | Structured semantic provider tests |
| Remote/hybrid LLM | v0.9.0 | NOT STARTED | Policy/privacy/budget tests |
| Production-ready integration | v1.0.0 | NOT STARTED | Full acceptance suite |

## Phase 1F.1 — RBAC CLI safe-failure hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1G ready for independent review
- **Safe Operational Boundary:** `ipsp-sync-rbac` now converts the finite expected set of IPSP,
  migration-state, SQLAlchemy, and Pydantic settings failures into one generic non-zero CLI result.
  Raw exception text, SQL, database URLs and paths, configuration values, stack traces, and
  password/session/CSRF/token markers are never printed; `KeyboardInterrupt` and `SystemExit` remain
  unswallowed
- **Resource Cleanup:** Once foundation services exist, engine disposal is guaranteed for successful,
  no-op, stale-migration, migration-inspection, and database-inspection outcomes, including process
  control exceptions
- **Regression Evidence:** Focused tests preserve successful and idempotent synchronization, prove
  safe below-head refusal, inject `MigrationStateError`, SQLAlchemy inspection failure, and invalid
  settings, verify marker suppression, and assert post-construction engine disposal
- **Test Evidence:** `pytest` — 145 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall, Ruff lint/format for 73 files, strict mypy for 52 source files,
  `pip check`, and `git diff --check` passed. `pyproject.toml`, `requirements.lock`, migration head
  `20260811_03`, and the five-table ORM allowlist remain unchanged by this hardening pass
- **Architecture Decisions Added:** None; this is a narrow Phase 1F CLI failure-boundary correction
  and introduces no Phase 1G implementation

Phase 1 and v0.1.0 remain in progress. Phase 1G has not begun and remains subject to independent
review of this hardening pass.

## Phase 1F — RBAC Permission Enforcement

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; ready for independent review before Phase 1G
- **Runtime Authority:** `User.role_id → Role → RolePermission → Permission` is the sole permission
  path. `RBACService.has_permission` performs a fresh fail-closed database query, and
  `enforce_permission` raises the safe `PermissionDeniedException` mapped to HTTP 403
  `AUTHZ-PERMISSION_DENIED`. There is no role-name, persisted Admin Boolean, wildcard, access-level,
  cookie, session, or cached permission shortcut
- **Core Catalog:** A typed first-party `CorePermission` catalog contains exactly the 13 frozen codes:
  `simulation.run`, `simulation.export`, `dataset.view`, `dataset.upload`, `dataset.configure`,
  `dataset.assign`, `model.train`, `model.promote`, `llm.configure`, `internet.configure`,
  `user.manage`, `logs.view`, and `system.configure`. Persisted permission strings remain extensible
- **Provisioning:** Additive, idempotent synchronization ensures Admin/User roles, all 13 core
  Permission rows, and 13 explicit Admin mappings. User receives no automatic grants, and custom
  roles, permissions, and mappings are preserved without pruning. Admin is usable only because of
  its mappings, not its name
- **API Boundary:** The reusable permission dependency authenticates first, resolves the composed
  RBAC service, and enforces using the authenticated user ID. Temporary integration routes prove
  401 authentication precedence, safe 403 denials, allowed mapped access, and independent CSRF plus
  RBAC composition for state-changing requests; no new production endpoint was added
- **Privilege Changes:** Narrow transactional primitives change a user's role or replace a role's
  mappings and invalidate all active sessions for exactly the affected users. Same-role and
  identical-mapping operations are no-ops. Catalog privilege expansion invalidates existing Admin
  users' sessions while no-op synchronization and unrelated-role sessions remain valid
- **Bootstrap and Existing Installations:** Fresh `ipsp-create-admin` now provisions the catalog and
  creates the first Admin with explicit mappings. `ipsp-sync-rbac` requires the database at current
  migration head, supports databases with users, reports only safe counts, and is repeatable
- **Schema and Dependencies:** No table, column, session snapshot, or Alembic migration was added;
  head remains `20260811_03` and the five-table ORM allowlist is unchanged. No dependency was added,
  `requirements.lock` is unchanged, and `pyproject.toml` changed only for `ipsp-sync-rbac`
- **Test Evidence:** `pytest` — 140 passed, 0 failed, 0 skipped, 0 warnings, including catalog,
  extensibility, anti-bypass, fail-closed matrix, dependency/CSRF, bootstrap/CLI, runtime freshness,
  privilege invalidation, and all Phase 1E/1E.1 authentication regressions
- **Quality Evidence:** Compileall, Ruff lint/format, strict mypy, `pip check`, `git diff --check`,
  Alembic heads/current/check, architecture scans, and runtime-artifact checks passed
- **Architecture Decisions Added:** None; Phase 1F implements locked decision D-016 without beginning
  Phase 1G durable audit/observability work

Phase 1 and v0.1.0 remain in progress. General user management, dataset ACL, and durable audit
persistence remain incomplete; Phase 1G must not begin until Phase 1F receives independent review.

## Phase 1E.1 — Authentication side-channel and regression hardening

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; Phase 1F ready for independent review
- **Authentication Failure Equalization:** Unknown, disabled, and currently locked login attempts now
  each perform exactly one dummy Argon2 verification. Active wrong-password and successful attempts
  each perform one real verification without an additional dummy operation. All four public failure
  classes retain the identical safe `AUTH-INVALID_CREDENTIALS` HTTP 401 response
- **Dummy Credential Policy:** `PasswordService` constructs its non-secret dummy Argon2 hash once
  with the same active `PasswordHash.recommended()` policy used for production hashes. It is not
  hard-coded, generated per request, or capable of authenticating
- **CSRF Regressions:** Integration coverage now proves a present CSRF header with a missing CSRF
  cookie is rejected, and a CSRF cookie/header from one valid session cannot authorize a different
  valid bearer session. Existing missing-header, mismatch, persisted-hash, Unicode, and leak checks
  remain intact
- **Session Fixation Regression:** An explicitly attacker-selected session cookie is replaced by a
  fresh server-generated bearer token at login; neither its raw value nor its digest becomes the
  authenticated session, while the stored SHA-256 digest matches only the newly issued token
- **Test Evidence:** `pytest` — 125 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall, Ruff lint and format, strict mypy, `pip check`, and
  `git diff --check` passed. Dependency files, migration history, and the five-table ORM allowlist
  remained unchanged
- **Architecture Decisions Added:** None; this is a narrow correction within the frozen Phase 1E
  authentication architecture and introduces no Phase 1F permission enforcement

Phase 1 and v0.1.0 remain in progress. Phase 1F must not begin until this hardening pass receives
independent review.

## Phase 1E — Authentication & Server-Side Session Security

- **Implementation Status:** COMPLETE (2026-08-12)
- **Gate Result:** PASS; ready for independent review before Phase 1F
- **Passwords:** Maintained `pwdlib[argon2]` produces Argon2id hashes, supports verify-and-update,
  preserves bounded Unicode input, and performs a real dummy Argon2 verification for unknown users.
  No plaintext, bcrypt, passlib, JWT, pepper, or generated default password path exists
- **Sessions:** Every successful login generates independent 256-bit-or-greater opaque session and
  CSRF tokens. Only deterministic SHA-256 hashes are stored in `user_sessions`; bearer values remain
  cookies only. Sessions use fixed expiry, UTC timestamps, last-seen updates, fresh non-secret UUID
  correlation IDs, fixation protection, logout invalidation, and user-scoped all-session invalidation
- **Browser Security:** Central cookie helpers set the session cookie HttpOnly and both cookies
  Secure by default, SameSite `lax`, Path `/`, and aligned expiry. Production rejects insecure-cookie
  configuration; explicit insecure cookies are limited to development/localhost HTTP. Authenticated
  logout and password change enforce the readable CSRF-cookie/header/hash contract
- **Login & Identity:** Generic authentication failures conceal unknown, wrong-password, disabled,
  and locked states. Failed attempts increment the persisted counter, apply temporary lockout at the
  configured threshold, and reset after an eligible successful login. Disabled users cannot log in
  or continue old sessions. Safe identity context resolves role ID/name but no permissions
- **API:** Thin `/api/v1/auth/login`, `/me`, `/logout`, and `/change-password` routes use explicit
  Pydantic `SecretStr` requests, safe response schemas, reusable session/CSRF dependencies, stable
  IPSP errors, no-store responses, and no bearer values in JSON
- **Password Change:** Current-password verification precedes persisted replacement; success updates
  the Argon2id hash and UTC password timestamp, clears forced-change and lock state, invalidates every
  session for that user, clears cookies, and leaves other users' sessions unchanged
- **Bootstrap:** The interactive `ipsp-create-admin` CLI requires an already migrated empty database,
  reads/confirm passwords with `getpass`, ensures only the canonical Admin/User role rows, assigns the
  first user to Admin, creates no permission mappings, and refuses subsequent bootstrap attempts
- **Migration:** Revision `20260811_03` directly descends from `20260811_02`, creates only
  `user_sessions`, downgrades only that table, re-upgrades cleanly, leaves one head, and retains the
  five-table ORM allowlist
- **Dependencies:** Added `pwdlib[argon2]>=0.3.0,<0.4`; the Python 3.12 lock resolves pwdlib 0.3.0,
  argon2-cffi 25.1.0, argon2-cffi-bindings 25.1.0, cffi 2.1.1, and pycparser 3.0
- **Test Evidence:** `pytest` — 121 passed, 0 failed, 0 skipped, 0 warnings, covering password,
  settings, session schema/lifecycle, login/lockout, cookies, identity, CSRF, logout, password change,
  disabled users, scoped invalidation, bootstrap, readiness, leak markers, and conformance behavior
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 68 files;
  strict mypy passed for 48 source files; `pip check`, `git diff --check`, and the isolated Alembic
  upgrade/current/check/downgrade/re-upgrade smoke passed
- **Clean Environment Evidence:** The exact lock installed in a disposable Python 3.12.0 environment;
  IPSP installed with `--no-deps`; all 121 tests, Ruff checks, strict mypy, compileall, and `pip check`
  passed, after which the environment was removed
- **Architecture Decisions Added:** None; Phase 1E implements the frozen authentication authorities
  and intentionally does not implement RBAC permission enforcement or Admin-name authorization

Phase 1 and v0.1.0 remain in progress. RBAC permission enforcement remains owned by Phase 1F and
must not begin until Phase 1E receives independent review.

## Phase 1D — User / Role / Permission Security-Schema Foundation

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for independent review before Phase 1E
- **Schema:** Canonical typed SQLAlchemy 2.x mappings add exactly `roles`, `permissions`,
  `role_permissions`, and `users`. Model metadata contains no other tables, and the migration inserts
  no production role, permission, mapping, user, password, or credential data
- **Authorization Structure:** `User.role_id → Role → RolePermission → Permission` is the only
  structural authorization path. Role-permission mappings use a composite primary key, and no
  persisted `is_admin`, equivalent bypass Boolean/level, permission blob, wildcard, or role hierarchy
  exists
- **User Schema:** The frozen minimum identity/lifecycle fields are present; username is unique,
  email and creator are nullable, role is required, creator is a self-FK, lifecycle defaults agree
  between ORM and migration, and `failed_login_count >= 0` is enforced intrinsically
- **UTC Boundary:** One reusable `UTCDateTime` rejects naive input, normalizes aware values to UTC
  before SQLite persistence, and restores aware UTC datetimes. UTC, `+05:30`, nullable, default, and
  all-security-timestamp round trips pass on real SQLite
- **Migration:** Revision `20260811_02` directly descends from `20260811_01`, creates only the four
  authorized tables, downgrades cleanly to the Phase 1C baseline, re-upgrades cleanly, leaves one
  script head, and passes `alembic check`
- **Constraint Evidence:** Real SQLite inserts prove username, role name, permission code, and mapping
  uniqueness; user role, self-creator, and both mapping FKs; and non-negative failed-login enforcement
- **ORM Evidence:** Canonical session transactions insert all four entities and query them using
  `select()`, `Session.execute()`, `Session.scalars()`, and an explicit
  `User → Role → RolePermission → Permission` join without a repository or RBAC service
- **Readiness:** A Phase 1D-head database returns HTTP 200; a Phase 1C-baseline database returns HTTP
  503 with `SYS-MIGRATION-REQUIRED`; FK-disabled readiness and database-independent liveness remain
  unchanged
- **Dependencies:** No direct or resolved dependency changes; `pyproject.toml` and
  `requirements.lock` remain unchanged
- **Test Evidence:** `pytest` — 101 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 53 files;
  strict mypy passed for 36 source files; `pip check` and `git diff --check` passed
- **Conformance Evidence:** The exact four-table allowlist, sole ORM/Alembic ownership, synchronous
  SQLAlchemy, no production `create_all()`, no authorization bypass, no session/preference tables, no
  authentication/RBAC/password behavior, and all prior framework/network/contamination guards pass
- **Intentionally Deferred:** Password hashing, login/logout, sessions, cookies, CSRF, lockout
  behavior, authentication routes, bootstrap administration, and RBAC permission enforcement remain
  owned by Phase 1E/1F
- **Architecture Decisions Added:** None; Phase 1D implements locked decisions D-004, D-014, D-015,
  D-016, and the security schema authorities

Phase 1 and v0.1.0 remain in progress. Phase 1E functionality was not introduced and must not begin
until Phase 1D receives independent review.

## Phase 1C.1 — Database foundation hardening

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; Phase 1D ready for independent review
- **H-001 Readiness Semantics:** Healthy readiness returns HTTP 200; migration-required,
  database-unavailable, FK-disabled, and invalid migration-state responses return HTTP 503 with the
  same minimal safe response contract. Liveness remains HTTP 200 and database-independent
- **H-002 SQL Parameter Privacy:** Every engine forces SQLAlchemy `hide_parameters=True`; echo and
  `StatementError` regression coverage proves the `DO_NOT_LEAK_DATABASE_PARAMETER` bound value is
  absent from captured logs, output, and rendered errors
- **H-003 Deterministic Default:** The no-environment default resolves through SQLAlchemy URL
  utilities to `<repository>/database/ipsp.db` and remains unchanged when the process CWD changes.
  `.env.example` leaves the optional absolute URL override commented out
- **H-004 Synchronous Driver Restriction:** Database URL validation accepts only `sqlite` and
  `sqlite+pysqlite`; `sqlite+aiosqlite`, non-SQLite, malformed, credential-bearing, and host-bearing
  URLs fail closed without installing another driver
- **H-005 FK Readiness:** Readiness now requires `PRAGMA foreign_keys=1`. Tests verify two distinct
  DBAPI connection lifecycles and prove a real test-only invalid child insert raises an integrity error
- **H-006 Migration Heads:** Script and database inspection use multi-head APIs, require one script
  head, allow zero database heads before migration, accept one matching head, and convert multiple or
  malformed heads into a safe migration-state failure and HTTP 503
- **H-007 Conformance:** Automated guards now cover frontend frameworks, Streamlit, legacy and async
  SQLAlchemy, aiosqlite, production `create_all()`, duplicate Declarative Bases/Alembic roots,
  Phase-1C business tables, runtime CDNs, JWT libraries, outbound HTTP clients, Redis, and Celery. The
  no-business-table assertion is explicitly documented as a Phase-1C-only guard for Phase 1D evolution
- **Dependencies:** No direct or resolved dependency changes; `pyproject.toml` and
  `requirements.lock` remain unchanged
- **Test Evidence:** `pytest` — 84 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 49 files;
  strict mypy passed for 34 source files; `pip check` and `git diff --check` passed
- **Architecture Decisions Added:** None; this hardening pass corrects reviewed Phase 1C behavior
  within locked decisions D-004, D-014, and D-015

Phase 1 and v0.1.0 remain in progress. Phase 1D functionality was not introduced and remains blocked
until Phase 1C.1 receives independent review.

## Phase 1C Status

**Phase 1C - Synchronous SQLite Control-Plane Foundation & Alembic Baseline**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for independent review before Phase 1D
- **Configuration:** Immutable nested `IPSP_DATABASE__URL`, `IPSP_DATABASE__ECHO`, and
  `IPSP_DATABASE__CONNECTION_TIMEOUT_SECONDS` settings now configure the control plane. Only
  credential-free SQLite URLs are accepted; unsupported or malformed URLs fail closed
- **Database Foundation:** One canonical `DeclarativeBase` and `MetaData` with deterministic naming
  conventions live under `backend/ipsp/database/models/`. The explicit synchronous engine enables
  SQLite foreign keys on every connection and applies the configured timeout without global engines,
  automatic schema creation, WAL policy, or asynchronous SQLAlchemy
- **Sessions:** The typed session factory always closes sessions, never commits implicitly, commits
  only through an explicit transaction scope, and rolls failed transactions back
- **Migrations:** Root `alembic.ini` and the sole history under `database/migrations/` support online
  and offline execution through application Settings. The `20260811_01` no-op foundation baseline
  creates no business entity tables, and upgrade/current/downgrade/re-upgrade/check flows pass
- **Migration State & Readiness:** Side-effect-free revision inspection reports current revision,
  expected head, and head alignment. Readiness actively checks configuration, SQLite connectivity,
  and migration head with safe status codes; analytical storage and job workers remain explicitly
  deferred, while liveness remains database-independent
- **Dependencies:** Added maintained SQLAlchemy 2.0 and Alembic 1.x direct constraints. The exact
  Python 3.12 lock snapshot records SQLAlchemy 2.0.51, Alembic 1.19.1, and required transitive packages
- **Test Evidence:** `pytest` - 75 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 49 files;
  strict mypy passed for 34 source files; `pip check` and `git diff --check` passed
- **Clean Environment Evidence:** The exact lock installed in a fresh Python 3.12.0 virtual
  environment; the local package installed with no dependency resolution; all tests, Ruff checks,
  strict mypy, compileall, and `pip check` passed there
- **Conformance Evidence:** Exactly one Alembic root; no business/auth/RBAC/job ORM tables; no
  `create_all()`, legacy `Session.query()`, asynchronous SQLAlchemy, benchmark-specific production
  constants, runtime CDN, or prohibited architecture patterns
- **Architecture Decisions Added:** None; Phase 1C implements locked decisions D-004, D-014, and D-015

Phase 1 and v0.1.0 remain in progress. Phase 1D functionality was not introduced and must not begin
until Phase 1C receives independent review.

## Phase 1B Status

**Phase 1B — Configuration, SecretProvider, Feature Flags & Outbound Policy**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for independent review before Phase 1C
- **Configuration:** One immutable Pydantic Settings tree now separates runtime values, safe-off
  feature flags, secret-provider selection, and deny-by-default outbound permissions using canonical
  `IPSP_FEATURES__*`, `IPSP_OUTBOUND__*`, and `IPSP_SECRETS__*` environment variables
- **Secrets:** `SecretProvider`, validated `SecretRef`, redacted `SecretValue`, and the approved
  environment-injected provider are implemented. Required resolution fails closed without generated
  defaults, plaintext errors, configuration fields, logging, or ordinary JSON serialization
- **Outbound Policy:** Side-effect-free evaluation and enforcement cover global Internet, remote LLM,
  model-download, update-check, provider allowlisting, all five frozen transmission levels, explicit
  dataset-policy inputs, restricted-data local-only defaults, and context-sensitive fail-closed rules
- **Composition:** The app factory explicitly constructs immutable foundation services and exposes
  them through application state without mutable globals or a general service locator
- **Dependencies:** No direct or resolved dependency changes; `pyproject.toml` and
  `requirements.lock` remain unchanged
- **Test Evidence:** `pytest` — 59 passed, 0 failed, 0 skipped, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 41 files;
  strict mypy passed for 30 source files; `pip check` and `git diff --check` passed
- **Security Evidence:** The `DO_NOT_LEAK_PHASE1B_SECRET` marker remained absent from repr/str,
  configuration snapshots, Pydantic/JSON serialization, API error details, structured logs, secret
  lookup failures, and outbound-policy denials
- **Conformance Evidence:** Benchmark/business-term, Streamlit, legacy `Session.query()`, runtime CDN,
  JWT/browser-auth, actual network-call, and premature database/auth/upload/analytics scans passed
- **Intentional Extension Point:** Protected OS, vault, and cloud secret backends remain future
  `SecretProvider` implementations because no technology is frozen; approved environment injection
  is the production provider implemented in this phase
- **Architecture Decisions Added:** None; Phase 1B implements existing frozen configuration,
  privacy, secrets, and outbound-policy authorities

Phase 1 and v0.1.0 remain in progress. Phase 1C functionality was not introduced and must not begin
until Phase 1B receives independent review.

## Phase 1A.1 Status

**Phase 1A.1 — Foundation hardening**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; Phase 1B ready for independent review
- **H-001:** Domain error details now use a recursively sanitized client-safe contract, including
  final response-boundary sanitization and safe handling of unsupported objects
- **H-002:** Structured metadata redaction now recognizes case-insensitive password, token, secret,
  API-key, authorization, and cookie credential forms using deterministic exact/suffix rules
- **H-003:** Completed-request events derive `success` or `failure` from the actual HTTP status
- **H-004:** The JSON formatter emits supplied approved optional IPSP context through an explicit
  allowlist and does not serialize arbitrary `LogRecord` extras
- **H-005:** Egg-info, bytecode, pytest, mypy, and Ruff artifacts are ignored and none are tracked
- **H-006:** The existing lock snapshot installed successfully in a fresh Python 3.12.0 virtual
  environment; `pip check`, local `--no-deps` package installation, all eight direct constraints,
  compile, tests, Ruff lint/format, and strict mypy passed. Exact transitive portability to other
  Python versions was not claimed or tested
- **Test Evidence:** `pytest` — 26 passed, 0 failed, 0 warnings
- **Quality Evidence:** Compileall passed; Ruff lint passed; Ruff format check passed for 34 files;
  strict mypy passed for 26 source files; `pip check` and `git diff --check` passed
- **Conformance Evidence:** Benchmark/business-term, Streamlit, legacy `Session.query()`, runtime CDN,
  hardcoded campaign/demo output, and JWT/browser-auth scans passed
- **Architecture Decisions Added:** None; this pass implements existing frozen safety requirements

Phase 1 remains in progress. Phase 1B functionality was not introduced, and the full v0.1.0
milestone is not marked complete.

## Phase 1A Status

**Phase 1A — Minimal Production Foundation Skeleton**

- **Implementation Status:** COMPLETE (2026-08-11)
- **Gate Result:** PASS; ready for Phase 1B review
- **Implemented Scope:** FastAPI application factory, canonical versioned and health routes,
  environment-backed settings, safe central error envelopes, request/trace context, structured
  redacted logging, honest readiness checks, job contracts/enums, offline vanilla frontend shell,
  dark/light theme foundation, repository tooling, and meaningful automated tests
- **Intentionally Deferred:** Authentication, database schema/models, migrations, upload and data
  workflows, analytical execution, ML, LLM integration, simulation, and distributed job execution
- **Test Evidence:** `pytest` — 19 passed, 0 failed, 0 warnings
- **Quality Evidence:** Ruff lint passed; Ruff format check passed for 32 files; strict mypy passed
  for 25 source files; live Uvicorn liveness/readiness/frontend smoke probe passed
- **Conformance Evidence:** Benchmark/business-term, Streamlit, legacy `Session.query()`, runtime CDN,
  hardcoded campaign/demo output, and JWT/browser-auth scans passed
- **Architecture Decisions Added:** None; implementation follows the frozen authority set

Phase 1 remains in progress. Phase 1B must be separately reviewed and executed; this entry does not
mark the full v0.1.0 milestone complete.

## Phase 0.5 Status

**Phase 0.5 — Architecture Correction + Documentation Reconciliation**

- **Audit Status:** COMPLETE (2026-08-11)
- **Correction Execution:** COMPLETE (2026-08-11)
- **Findings:** 19 cross-document findings plus 5 completeness improvements; all resolved
- **Reconciliation Report:** [PHASE_0_5_RECONCILIATION_REPORT.md](PHASE_0_5_RECONCILIATION_REPORT.md)
- **Files Modified:** See reconciliation report and execution summary for the comprehensive list
- **Completion Gate:** 20/20 criteria verified

**Phase 1 Status:** 🟢 **READY** — Phase 0.5 completion gate passed

**Phase 0.5 PASS Criteria:**
```
✅ 1. Independent admin authorization removed
✅ 2. SQLAlchemy ORM ownership unified under database/models/
✅ 3. Duplicate ORM guidance removed; Pydantic API schemas separated
✅ 4. Synchronous SQLAlchemy 2.x execution model locked
✅ 5. Fake async database/repository guidance removed
✅ 6. Legacy Session query guidance removed
✅ 7. Alembic migration root unified under database/migrations/
✅ 8. API route ownership unified under api/routes/
✅ 9. Session lifecycle security complete
✅ 10. Raw bearer tokens excluded from logs; session_correlation_id specified
✅ 11. Production secrets fail closed
✅ 12. Runtime CDN dependencies prohibited; assets vendored
✅ 13. Dark/light theme foundation included in v0.1.0
✅ 14. Dataset/semantic/capability/model/run references immutable
✅ 15. Multi-table status derived rather than persisted twice
✅ 16. Audit envelope and log-sink policy reconciled
✅ 17. Job contracts/schema included in v0.1.0
✅ 18. Liveness/readiness/Admin diagnostics separated
✅ 19. Documentation consistency and contamination scans passed
✅ 20. Reconciliation report and progress status updated after verification
```

Update this file after each phase. Do not mark complete without test evidence.
