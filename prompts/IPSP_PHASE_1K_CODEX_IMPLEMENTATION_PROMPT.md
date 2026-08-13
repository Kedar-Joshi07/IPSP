# IPSP v1.0 — Phase 1K Codex Implementation Prompt
## Foundation Integration & Security Test Consolidation

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `da5e818f29964029a9af26fbf85dd8bce51a12e0`

Current independently reviewed state:

- Phase 0 / 0.5: PASS
- Phase 1A / 1A.1: FINAL PASS
- Phase 1B: FINAL PASS
- Phase 1C / 1C.1: FINAL PASS
- Phase 1D: FINAL PASS
- Phase 1E / 1E.1: FINAL PASS
- Phase 1F / 1F.1: FINAL PASS
- Phase 1G / 1G.1: FINAL PASS
- Phase 1H / 1H.1 / 1H.2: FINAL PASS
- Phase 1I: FINAL PASS
- Phase 1J / 1J.1 / 1J.2: FINAL PASS
- Phase 1K: AUTHORIZED
- Application version remains `v0.1.0`

This task is **Phase 1K only**.

Phase 1K is primarily a **proof, integration, and adversarial-security phase**, not a feature-building phase.

The objective is to exercise the completed Phase 1 foundation as one system, close meaningful test gaps across subsystem boundaries, and prove that the security architecture still behaves correctly when authentication, authorization, jobs, observability, health, configuration, SQLite, and the frontend are used together.

Phase 1L remains the final Phase 1 acceptance audit after independent review of Phase 1K.

Do not begin Phase 1L.

---

# 1. Frozen Phase 1K principle

Use this rule throughout:

> **Phase 1K verifies implemented foundation contracts. It does not pull future IPSP capabilities forward.**

Phase 1K must not implement acceptance criteria that belong to later milestones, including:

- dataset ingestion;
- dataset ACLs;
- Parquet analytical storage;
- profiling;
- semantic discovery;
- relationship inference;
- capability discovery;
- model training;
- simulation;
- trust engine;
- LLM providers;
- backup/restore execution;
- reports/PDF/Excel;
- project management;
- dataset assignment;
- dynamic simulation UI.

The full V1.0 acceptance document includes those later requirements. They are **not Phase 1K failures** because their implementation phases have not begun.

Phase 1K covers only the v0.1.0 foundation that actually exists.

---

# 2. Read before editing

Read completely:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_PROJECT_STRUCTURE.md`
6. `docs/05_UI_UX_SPEC.md`
7. `docs/06_UI_DESIGN_SYSTEM.md`
8. `docs/18_SECURITY_RBAC_SPEC.md`
9. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
10. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
11. `docs/23_ERROR_HANDLING_SPEC.md`
12. `docs/27_SQLITE_SCHEMA_SPEC.md`
13. `docs/28_REST_API_CONTRACT.md`
14. `docs/29_TEST_STRATEGY.md`
15. `docs/30_ACCEPTANCE_CRITERIA.md`
16. `docs/31_IMPLEMENTATION_PROGRESS.md`
17. `docs/34_CODING_STANDARDS.md`
18. `docs/35_CONFIGURATION_SPEC.md`
19. `docs/37_SYSTEM_HEALTH_SPEC.md`
20. `docs/40_ANTI_CONTAMINATION.md`
21. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Then inspect all current tests:

```text
tests/unit/*
tests/integration/*
tests/security/*
tests/architecture/*
tests/conftest.py
```

Inspect production code relevant to Phase 1:

```text
backend/ipsp/main.py
backend/ipsp/config/*
backend/ipsp/security/*
backend/ipsp/database/*
backend/ipsp/repositories/*
backend/ipsp/auth/*
backend/ipsp/observability/*
backend/ipsp/jobs/*
backend/ipsp/services/readiness.py
backend/ipsp/services/system_health.py
backend/ipsp/api/*
backend/ipsp/cli/*
frontend/*
```

Before editing:

```text
git status --short
git rev-parse HEAD
```

Start from a clean tracked worktree except known user-owned prompt files.

---

# 3. Phase 1K implementation policy

Prefer a **tests-first / tests-mostly** change.

Expected primary changes are under:

```text
tests/integration/
tests/security/
tests/architecture/
docs/31_IMPLEMENTATION_PROGRESS.md
```

Small test helpers/fixtures are allowed.

Production code changes are allowed **only if a deterministic Phase 1K regression exposes an actual violation of an already-frozen Phase 1 contract**.

If production code must change:

1. name the defect;
2. write the failing deterministic regression first;
3. make the narrowest correction;
4. do not redesign the subsystem;
5. do not add architecture;
6. report every production file changed and why;
7. do not silently convert Phase 1K into a hardening/feature phase.

If no production defect is found, production source should remain unchanged.

---

# 4. Phase 1K deliverables

Build a consolidated foundation test layer proving these cross-system areas:

1. fresh isolated database/startup behavior;
2. first-admin bootstrap and authenticated application flow;
3. session/cookie/CSRF lifecycle;
4. RBAC authority and live privilege changes;
5. observability/audit/trace privacy;
6. job lifecycle through authenticated APIs and local worker;
7. liveness/readiness/Admin-health integration;
8. outbound/secrets/offline security boundaries;
9. frontend/browser integration against real same-origin APIs;
10. static/frontend path/security boundaries;
11. error-envelope/privacy behavior;
12. application restart/recovery behavior;
13. architecture/dependency/schema invariants;
14. deterministic security regression matrix.

Do not merely duplicate every existing unit test. Add integration value by crossing component boundaries.

---

# 5. Recommended new test ownership

Prefer cohesive files such as:

```text
tests/integration/test_phase1_foundation_e2e.py
tests/security/test_phase1_security_boundaries.py
```

Exact names may differ.

Do not create many tiny files with one assertion each.

Existing focused tests should remain where they are.

If an existing file is the natural owner for a regression, extend it rather than duplicating setup.

---

# 6. Test isolation requirements

Every Phase 1K integration/security test must be isolated.

Use:

- temporary SQLite databases;
- temporary log/data/artifact directories;
- migrated isolated DBs;
- deterministic users/roles/jobs;
- injected safe marker values.

Do not:

- modify the default developer DB;
- depend on prior test order;
- depend on existing local users;
- depend on real Internet;
- use real credentials;
- leave log/DB/WAL/SHM residue;
- use the user's home directory;
- depend on current wall-clock timing where a timestamp can be injected;
- use arbitrary sleeps for synchronization.

Tests must be independently repeatable.

---

# 7. Fresh database and startup integration

Prove the lifecycle from an isolated database.

## 7.1 Before migration head

With a DB that is absent/unmigrated or intentionally behind head:

```text
application process can be constructed where expected
/health/live -> 200
/health/ready -> 503
worker is not falsely reported ready
safe migration/system error code
no DB path/SQL/exception leak
```

Use the already-frozen readiness behavior; do not invent a new failure code if one already exists.

## 7.2 At migration head

After isolated migration to:

```text
20260812_05
```

prove:

```text
application lifespan starts
local worker starts
/health/live -> 200
/health/ready -> 200
job_worker -> ready
runtime_logs -> ready
analytical_storage remains deferred
frontend root/API root available
```

## 7.3 Shutdown

After lifespan exit:

- no non-daemon worker leak;
- no application hang;
- no false job completion;
- test DB can be disposed/removed;
- repeated app lifecycle still works.

Do not weaken the existing non-cooperative subprocess regression.

---

# 8. First-admin bootstrap end-to-end

Use an isolated migrated DB.

Exercise the real foundation bootstrap path, preferably through:

```text
bootstrap_first_admin(...)
```

and/or the canonical CLI logic without exposing passwords.

Prove:

1. bootstrap requires migration head;
2. first bootstrap creates exactly one active user;
3. the user receives the canonical `Admin` role;
4. canonical RBAC catalog exists;
5. password storage is an Argon2id hash, never plaintext;
6. first Admin has permission mappings through Role → RolePermission → Permission;
7. a second bootstrap is rejected;
8. rejected bootstrap does not leak the submitted password;
9. bootstrap audit event exists;
10. bootstrap output/error handling does not expose hashes/secrets.

Do not authorize because role name is Admin; this test confirms bootstrap composition only.

---

# 9. Authenticated browser/API foundation journey

Using the bootstrapped user or isolated canonical users, prove an integrated flow such as:

```text
migrated DB
    ↓
bootstrap/provision identity
    ↓
POST /auth/login
    ↓
GET /auth/me
    ↓
GET /health/ready
    ↓
GET /api/v1/jobs
    ↓
GET /api/v1/admin/system/health when permitted
    ↓
POST /auth/logout with CSRF
    ↓
GET /auth/me -> 401
```

Validate that:

- login response contains safe identity only;
- session credential is a cookie, not JSON;
- CSRF cookie is separate;
- frontend/browser bootstrap contains CSRF *names* only;
- logout invalidates the server session;
- stale session cannot be reused.

No browser localStorage authority.

---

# 10. Cookie/session security matrix

Add deterministic integration assertions for the actual cookie contract.

At minimum:

## Session cookie
- HttpOnly;
- SameSite configured;
- Secure when configured/production;
- no raw token in JSON;
- raw token not persisted in SQLite;
- token hash persisted instead.

## CSRF cookie
- distinct from session cookie;
- intentionally browser-readable;
- SameSite configured;
- Secure according to environment/config;
- server stores only CSRF hash;
- state-changing request requires matching cookie/header and stored session binding.

## Login/session rotation
Prove:

```text
existing session A
successful login with same browser
    -> old session invalidated
    -> new session token differs
```

Do not compare secrets by logging them.

## Logout
Prove session invalidation persists server-side.

## Expiry
Use injected timestamps or DB fixture state rather than sleeping.

## Disabled user
An existing session for a disabled user must stop authenticating and be invalidated.

---

# 11. CSRF adversarial matrix

Test browser state-changing routes across subsystem boundaries.

At minimum include:

```text
POST /api/v1/auth/logout
POST /api/v1/auth/change-password
POST /api/v1/jobs/{id}/cancel
POST /api/v1/jobs/{id}/retry
```

For representative routes prove:

- missing CSRF cookie/header -> rejected;
- cookie only -> rejected;
- header only -> rejected;
- mismatched values -> rejected;
- CSRF from another session -> rejected;
- correct bound cookie/header -> allowed if the underlying action is otherwise valid.

GET routes must not require CSRF.

Responses must not echo CSRF values.

Audit/security event for CSRF rejection must not contain raw tokens.

Do not invent double-submit-cookie behavior beyond the existing stored-hash binding.

---

# 12. Password-change integrated security

Prove:

```text
session A
session B for same user
password change from A
    ↓
all sessions invalidated
    ↓
old password no longer works
new password works
must_change_password clears according to current contract
```

Also prove:

- current-password failure uses safe error;
- invalid new password uses safe error;
- password/hash is absent from API response/log/audit;
- password change requires CSRF;
- current session is not silently retained after successful password change.

Use conspicuous secret markers and scan outputs/logs/audit.

---

# 13. Failed-login / lockout integration

Do not create flaky timing benchmarks.

Use deterministic timestamps/service injection where possible.

Prove:

- repeated invalid passwords increment failure state;
- threshold produces temporary lock;
- correct password during lock does not authenticate;
- expired lock permits normal login;
- successful login resets failed-login state;
- unknown/disabled/locked identities still receive generic authentication failure externally;
- no account-existence information is leaked through error body/status.

Existing timing-equalization unit coverage must remain green; Phase 1K does not need wall-clock timing assertions.

---

# 14. RBAC integration matrix

The sole authority remains:

```text
User.role_id
    -> Role
    -> RolePermission
    -> Permission
```

Prove integrated server behavior, not just helper functions.

## 14.1 Permission mapping, not role name

Use an authorized endpoint such as:

```text
GET /api/v1/admin/system/health
```

Prove:

```text
non-Admin role + system.configure mapping -> 200
role named Admin without mapping           -> 403
ordinary user without mapping              -> 403
unauthenticated                            -> 401
```

## 14.2 Live privilege changes

With an existing active session:

- add/remove relevant permission mapping according to current supported administrative/service test path;
- verify authorization reads current DB authority rather than cached session snapshots;
- where the frozen contract requires privilege-change session invalidation, assert the current supported change path invalidates sessions.

Do not add a user-management API just for testing.

Use repositories/services directly when the public management API does not yet exist.

## 14.3 Session schema

Assert no role/permission snapshot or `is_admin` bypass exists in `user_sessions`.

Architecture test already checks this; preserve it.

---

# 15. Job API + worker + auth integration

Existing job lifecycle tests are extensive. Phase 1K should add only cross-layer proof that materially joins:

```text
authenticated identity
+ owner scoping
+ local worker
+ persisted job
+ API
+ observability/audit
+ readiness/health
```

Use a trusted **test-only handler** registered directly into the local worker infrastructure.

Do not create a public generic job-submit API.

A useful flow:

```text
internal service submits test job for User A
    ↓
worker claims/executes
    ↓
User A lists/views it via API
    ↓
User B cannot discover/view it
    ↓
progress/terminal state persists
    ↓
System Health/worker remains coherent
```

Also cover one integrated cancel/retry flow if not already sufficiently cross-layer.

Required privacy:

- cross-owner access is indistinguishable from not-found according to the frozen policy;
- artifact references remain text/safe references;
- job error remains safe;
- raw metadata/owner secret does not leak.

Do not duplicate all Phase 1H concurrency tests.

---

# 16. Restart/recovery integration

Preserve and integrate the existing recovery contract.

At minimum prove one real persisted interrupted job across worker/application lifecycle:

```text
job RUNNING
process/worker generation interrupted
fresh worker/app startup
    ↓
FAILED
JOB-WORKER-INTERRUPTED
retryable=true
```

The existing permanent blocked-handler subprocess proof must remain green.

Phase 1K may reuse it instead of building another heavy subprocess test.

Do not change the recovery code unless a deterministic integration test exposes a contract defect.

---

# 17. Liveness/readiness/Admin-health cross-boundary tests

Prove the three surfaces remain distinct under multiple failure states.

## Liveness
Always minimal process signal:

```text
status
timestamp_utc
```

No dependency details.

## Readiness
Minimal dependency state:

```text
application
configuration
database
foreign_keys
migration
runtime_logs
job_worker
```

and only:

```text
analytical_storage
```

deferred at this phase.

## Admin health
Permission-protected rich diagnostics.

Test representative degraded cases:

- worker unavailable;
- runtime log path invalid;
- DB/migration unavailable;
- no backup ever run;
- LLM not implemented;
- model artifacts not initialized.

Future/not-implemented components must not falsely make the whole foundation unhealthy when the Phase 1I contract says they are informational.

No public probe may expose rich Admin diagnostics.

---

# 18. Health endpoint privacy matrix

Seed conspicuous markers such as:

```text
DO_NOT_LEAK_PHASE1K_DB_PATH
DO_NOT_LEAK_PHASE1K_PASSWORD
DO_NOT_LEAK_PHASE1K_SESSION_TOKEN
DO_NOT_LEAK_PHASE1K_CSRF
DO_NOT_LEAK_PHASE1K_EXCEPTION
DO_NOT_LEAK_PHASE1K_LOG_METADATA
```

Ensure none appear in:

```text
/health/live
/health/ready
/api/v1/admin/system/health
```

Rich Admin access still does not justify:

- DB URL;
- absolute OS path;
- raw exception;
- raw log line;
- secret;
- token;
- password;
- SQL.

---

# 19. Observability and trace integration

Build at least one integrated request flow with explicit headers:

```text
X-Trace-ID
X-Request-ID
```

and verify correlation across:

- HTTP response headers;
- structured runtime event where appropriate;
- durable audit event where appropriate.

For authenticated events also verify:

```text
user_id
resolved_role
session_correlation_id
```

when the event context supplies them.

Required privacy:

- `session_correlation_id` is not raw session token;
- raw session cookie/token is absent from runtime logs;
- raw CSRF is absent;
- password/hash is absent;
- authorization header marker is absent;
- metadata is sanitized.

Do not require every request to create a durable audit event. Audit only actions that the established event model audits.

---

# 20. Error-envelope integration

Exercise representative failures across components:

```text
401 authentication
403 authorization
CSRF failure
404 owner-hidden job/not-found
safe 5xx/domain error
readiness 503
```

For central API errors prove:

```text
error_code
safe message
trace_id
recoverable
safe details if present
```

and:

```text
response trace_id == response X-Trace-ID
```

No raw Python traceback, exception string, SQL, filesystem path, secret, or request body.

Readiness 503 remains its own minimal HealthResponse contract rather than being forced into the normal error envelope.

---

# 21. Secret-provider / production-safety integration

Preserve existing SecretProvider tests and add only cross-system proof where useful.

Required assertions:

- production unsafe configuration fails closed;
- production cannot run with insecure auth-cookie policy;
- required secrets, where the current foundation actually requires them, are not silently randomly regenerated;
- ordinary Settings object contains non-secret configuration only according to current design;
- no `.env` secret value is written into SQLite/logs;
- secret-provider failures produce safe diagnostics.

Do not invent a new required secret if the current implementation does not need one.

Do not add vault/keyring/cloud providers.

---

# 22. Outbound/offline security integration

The foundation must be able to operate with:

```text
internet_enabled=false
remote_llm_enabled=false
model_download_enabled=false
update_check_enabled=false
```

Prove:

- application startup works offline;
- auth/jobs/health/frontend foundation works offline;
- System Health does not perform DNS/socket/HTTP probes;
- enabling a feature flag does not bypass backend `OutboundPolicy`;
- disallowed remote operation path in the existing policy service fails with the established safe error.

Do not add a remote provider merely to test denial.

If monkeypatching network primitives, use it only to prove the tested foundation flow performs no network call.

---

# 23. Frontend + real API integration

Phase 1J/1J.1/1J.2 already added strong static contracts and local browser QA.

Phase 1K should execute one integrated browser journey if the existing Codex/browser QA facility is available:

```text
fresh migrated isolated DB
bootstrap/provision user
start actual local app
open /
login
overview
jobs
profile
system health when authorized
theme switch
logout
```

Also test one denied System Health user:

```text
authenticated without system.configure
#/admin/system
    -> permission state
```

And one required-password user:

```text
login
required-password screen
normal navigation hidden
sign out works
```

Requirements:

- no browser errors/warnings;
- no external browser requests;
- no page overflow at desktop and ~390px mobile;
- route-race protections remain green;
- no auth identity/token persisted in localStorage;
- only `ipsp.theme` may persist;
- session cookie remains HttpOnly and unavailable to JS;
- frontend cannot authorize from role name.

Do not install Playwright/Selenium/npm for the project solely for this.

If Codex's external browser QA facility is unavailable, report it explicitly and rely on existing deterministic source/integration tests; do not add a new dependency.

---

# 24. Static asset/path security

Add deterministic tests around static hosting where meaningful.

Prove:

- `/` serves only the intended frontend;
- known `/css/...` and `/js/...` assets serve normally;
- `/api/v1` and `/health/...` are not shadowed by static routes;
- encoded/relative traversal attempts do not expose arbitrary repository/OS files;
- hidden source/config files are not made available through frontend static routing.

Do not add a generic backend catch-all.

Do not expose `.env`, SQLite DB, logs, source code, or repository parent paths through StaticFiles.

Use temp marker files outside `frontend_dir` to prove containment without reading real secrets.

---

# 25. Frontend security regression preservation

All prior guards remain mandatory.

No production JS:

```text
innerHTML
outerHTML
insertAdjacentHTML
document.write
eval(
new Function
```

Only `theme.js` may use:

```text
localStorage
```

Only `api.js` may read:

```text
document.cookie
```

No:

```text
sessionStorage
auth/token storage
role-name authorization
external asset URL
CDN
React/Vue/Angular/Svelte
Streamlit
benchmark marketing logic
BF1-BF8
ROAS/CPA/CTR demo contamination
```

Do not weaken these tests to get Phase 1K green.

---

# 26. Database durability/security checks

Across the integrated suite verify:

- foreign keys enabled;
- one canonical SQLAlchemy Base;
- seven ORM tables exactly;
- migration head `20260812_05`;
- no direct `create_all`;
- no async SQLAlchemy;
- no raw session token persisted;
- no raw CSRF persisted;
- no plaintext password;
- audit table remains append-only through repository contract;
- jobs persistence remains guarded by current state-machine transitions.

Do not add new DB tables.

---

# 27. Concurrency and thread-safety boundaries

Do not introduce broad stress/performance testing.

Preserve targeted deterministic concurrency guarantees:

- atomic job claim;
- worker generation authority;
- shutdown boundedness;
- context isolation;
- no stale frontend route writes;
- no duplicate frontend mutations;
- no double-submit auth/job mutations.

Any new concurrency test must use Events/Barriers/explicit state, not probabilistic sleeps.

---

# 28. Security marker sweep

Use conspicuous unique values across representative integration tests, for example:

```text
PHASE1K_PASSWORD_DO_NOT_LEAK
PHASE1K_SESSION_DO_NOT_LEAK
PHASE1K_CSRF_DO_NOT_LEAK
PHASE1K_AUTH_HEADER_DO_NOT_LEAK
PHASE1K_DBPATH_DO_NOT_LEAK
PHASE1K_METADATA_DO_NOT_LEAK
PHASE1K_EXCEPTION_DO_NOT_LEAK
```

After exercising auth/jobs/errors/health, inspect relevant:

- API responses;
- runtime JSONL logs;
- durable audit rows;
- safe System Health summary.

Assert secret markers are absent where prohibited.

Do not write the marker values into permanent repository fixtures.

---

# 29. Test quality requirements

Phase 1K tests must be:

- deterministic;
- readable;
- explicit about security expectation;
- focused on externally meaningful behavior;
- independent of run order;
- cross-platform where possible;
- bounded in runtime;
- not dependent on Internet;
- not dependent on user machine state.

Avoid:

- `time.sleep()` race tests;
- huge loops;
- brute-force fuzzing;
- fragile exact wall-clock timing;
- Unix-only chmod assumptions;
- hardcoded Windows paths;
- random retry until green;
- snapshotting enormous JSON blobs.

Use precise assertions.

---

# 30. No test-only production bypasses

Do not add production hooks such as:

```text
if TESTING:
skip_auth
skip_csrf
grant_admin
disable_rbac
disable_audit
disable_worker_authority
```

Injection of existing service/provider dependencies for deterministic tests is allowed where the architecture already supports it.

Never add a hidden bypass solely for tests.

---

# 31. Architecture-conformance strengthening

Strengthen `tests/architecture/test_conformance.py` only where Phase 1K reveals a meaningful frozen invariant not already covered.

Useful final Phase 1 invariants include:

- exact seven ORM tables;
- one DeclarativeBase;
- one Alembic tree;
- no async DB;
- no Redis/Celery;
- no role-name authorization;
- no persisted `is_admin`;
- no auth/session/permission snapshot in session;
- no production external network client;
- no unsafe frontend sinks;
- no framework/CDN;
- no Streamlit;
- no benchmark contamination;
- liveness/readiness/Admin health separated;
- LocalJobBackend remains single-process;
- frontend StaticFiles does not own `/api` or `/health`.

Do not turn conformance into brittle formatting assertions.

---

# 32. Phase 1K production-fix stop rule

If tests uncover a defect requiring any of the following, **stop and report FAIL instead of implementing it inside 1K**:

- new DB table/migration;
- new permission;
- public API redesign;
- auth/session architecture redesign;
- new worker provider;
- new dependency;
- new secret architecture;
- frontend framework/build tool;
- future dataset/model/simulation feature.

Such an issue requires a dedicated hardening phase before Phase 1L.

Small corrections to existing functions/contracts are allowed as described in Section 3.

---

# 33. Documentation

Update:

```text
docs/31_IMPLEMENTATION_PROGRESS.md
```

Add:

```text
Phase 1K — Foundation Integration & Security Tests
```

Record:

- test-only or tests-mostly nature;
- major integrated flows covered;
- security matrices added;
- browser QA evidence if available;
- any defects found/fixed;
- no future-domain implementation;
- no schema/dependency change;
- exact test/quality evidence.

Do not mark Phase 1 complete.

Do not mark v0.1.0 accepted.

State that Phase 1L remains the final acceptance audit pending independent review.

README should change only if testing exposes an inaccurate operational instruction.

---

# 34. Schema/dependency lock

Expected:

```text
Alembic head = 20260812_05
ORM tables = exactly 7
new migration = none
pyproject.toml = unchanged
requirements.lock = unchanged
package.json = absent
node_modules = absent
```

No new Python/browser dependency is expected.

Do not add:

- coverage.py;
- hypothesis;
- pytest-xdist;
- pytest-asyncio;
- playwright;
- selenium;
- psutil;
- new npm package.

Use the current toolchain.

---

# 35. Mandatory quality gates

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

Also run isolated migration verification:

```text
alembic heads
alembic current
alembic check
```

If needed, run `upgrade head` only against an isolated temporary database.

Never intentionally mutate the default developer DB.

Confirm:

```text
head = 20260812_05
tables = 7
no migration change
no dependency change
```

If the current browser QA facility is available, run the Phase 1K browser integration journey.

---

# 36. Runtime residue audit

Before final report, check for:

- SQLite test DBs;
- WAL/SHM files;
- runtime JSONL/logs;
- temp browser profiles;
- screenshots unless deliberately retained and documented;
- secret marker files;
- process/thread dumps;
- archives;
- node_modules;
- build/dist;
- test virtualenv;
- credentials/tokens/cookies.

Remove temporary Phase 1K artifacts.

Do not remove user-owned files.

---

# 37. Phase 1K acceptance gate

PASS only when all applicable foundation categories are green.

## Startup/database
- isolated migration behavior verified;
- pre-head not-ready safe;
- head startup ready;
- worker lifecycle coherent.

## Authentication
- first-admin bootstrap;
- Argon2id/password privacy;
- session rotation;
- expiry;
- logout;
- disabled-user behavior;
- lockout;
- password-change invalidation.

## CSRF
- correct binding;
- adversarial mismatch/cross-session rejection;
- all state-changing foundation routes protected.

## RBAC
- RolePermission is sole authority;
- role name not authority;
- live DB permission behavior;
- privilege/session invalidation preserved.

## Jobs
- authenticated owner-only integration;
- worker persistence;
- cancel/retry/recovery;
- privacy.

## Observability
- trace/request correlation;
- session correlation;
- audit/runtime separation;
- secret markers absent.

## Health
- liveness/readiness/Admin separation;
- public privacy;
- permission-protected diagnostics;
- representative degradation states.

## Outbound/secrets
- offline foundation;
- deny-by-default policy;
- no secret leakage;
- no network health probes.

## Frontend
- real API/auth journey;
- permission state;
- required-password flow;
- route lifecycle;
- theme;
- mobile/desktop;
- no external assets or unsafe DOM.

## Architecture
- exact seven tables;
- one migration root/head;
- no dependency/schema drift;
- no framework/domain contamination;
- Phase 1L not started.

## Quality
- full pytest green;
- zero skips unless an already-existing platform-conditional test has a documented reason;
- zero warnings;
- Ruff/mypy/compile/pip/diff/Alembic green.

---

# 38. Mandatory Codex final report

Return every section.

## A. Starting state
- starting SHA
- branch
- initial git status

## B. Files created
Every retained file.

## C. Files modified
Every file.

## D. Phase 1K strategy
Explain tests added, integration boundaries exercised, and why these add coverage beyond prior isolated tests.

## E. Fresh startup/database
Report pre-migration behavior, head migration behavior, readiness, worker lifecycle.

## F. Admin bootstrap
Report first admin, second-bootstrap denial, RBAC catalog, password storage, audit.

## G. Authentication/session
Report login, cookie flags, token hashing, rotation, expiry, logout, disabled user, lockout.

## H. CSRF
Report each route/matrix covered and cross-session behavior.

## I. Password change
Report validation, all-session invalidation, old/new password, privacy.

## J. RBAC
Report non-Admin mapped permission, Admin name without mapping, live privilege behavior, session invalidation behavior.

## K. Jobs
Report cross-layer authenticated flow, owner privacy, progress/terminal state, cancel/retry, recovery evidence.

## L. Observability/audit
Report trace/request propagation, user/role/session correlation, audit/runtime sinks, marker leak sweep.

## M. Health
Report live, ready, Admin, degradation cases, privacy.

## N. Outbound/secrets/offline
Report offline startup/use, policy denial, production safety, secret behavior, confirmation no real network dependency.

## O. Frontend/browser
Report browser journey if available, denied user, required-password user, desktop/mobile, external requests, console warnings/errors, storage/cookie boundary.

If browser QA unavailable, say so explicitly without installing a dependency.

## P. Error/privacy matrix
Report 401/403/404/CSRF/5xx/readiness 503 behavior and secret/path/traceback exclusions.

## Q. Architecture/conformance
Explicitly report ORM table allowlist, Alembic head/root, sync DB, no Redis/Celery, no role-name auth, no is_admin, no frontend framework/CDN, no Streamlit, no external health/network client, no benchmark contamination.

## R. Production defects found/fixed
If none:

`None — Phase 1K was tests/documentation only.`

If any, report exact defect, failing regression, production files changed, and why the correction stayed within frozen contract.

## S. Prior-phase regression
Confirm Phase 1A through Phase 1J.2 remain green.

## T. Tests
Exact passed/failed/skipped/warnings/duration.

## U. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, git diff check, Alembic heads/current/check, browser QA if available.

## V. Dependency/schema state
State pyproject, lock, migration, ORM, npm/package changes.

## W. Runtime artifacts
Report residue audit.

## X. Phase boundary
Confirm no Phase 1L or later-domain implementation.

## Y. Git state
Final status and diff stat.

## Z. Deviations / unresolved issues
If none:

`None`

## AA. Gate result

End exactly with one:

`Phase 1K: PASS — ready for independent review before Phase 1L`

or

`Phase 1K: FAIL — Phase 1L blocked`

Do not begin Phase 1L.
