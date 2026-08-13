# IPSP v1.0 — Phase 1L Codex Final Acceptance Audit Prompt
## v0.1.0 Foundation Release Gate

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting SHA:** `33a5901c67c706290c5f05087555dc315eff4cf4`

All earlier Phase 1 work through **Phase 1K has passed independent review**. Phase 1L is authorized.

This task is **Phase 1L only**. It is the final acceptance audit for the already-implemented `v0.1.0` foundation. It is not a feature phase and must not begin v0.2 ingestion work.

Do **not** create a Git tag or GitHub release. Do **not** authorize v0.2 yourself; independent review of the Phase 1L commit will decide that.

---

# 1. Governing rule

> Audit what Phase 1 was supposed to deliver. Do not judge the foundation as though v1.0 domain engines already exist, and do not implement future capabilities to make v1.0-wide acceptance criteria pass.

For audit rows use exactly:

- `PASS`
- `DEFERRED_BY_ROADMAP`
- `NOT_APPLICABLE`
- `BLOCKED`

`BLOCKED` means a requirement that belongs to Phase 1 is missing, broken, unsafe, or unverifiable.

Later-roadmap requirements such as ingestion, semantic discovery, models, simulation, trust, history, exports, LLM providers, dataset ACLs, and backup/restore execution must be marked `DEFERRED_BY_ROADMAP` where appropriate rather than treated as Phase 1 failures.

---

# 2. Final-audit stop rule

Phase 1L should be **audit/tests/documentation only**.

Expected PASS changes are limited to:

```text
docs/PHASE_1_ACCEPTANCE_REPORT.md
docs/31_IMPLEMENTATION_PROGRESS.md
README.md
tests/... only if a genuinely missing audit/conformance assertion is required
```

Production implementation should remain unchanged.

If the audit uncovers a real defect in an already-frozen Phase 1 contract:

1. retain deterministic evidence;
2. document the blocker;
3. mark Phase 1L FAIL;
4. do not patch production code inside Phase 1L;
5. do not mark Phase 1 complete;
6. do not begin or authorize v0.2.

A production defect must be handled later by a narrow Phase 1L.x hardening pass.

---

# 3. Read before auditing

Read completely:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `README.md`
4. `docs/00_SCOPE_FREEZE.md`
5. `docs/01_PROJECT_SPEC.md`
6. `docs/02_PRODUCT_REQUIREMENTS.md`
7. `docs/03_ARCHITECTURE.md`
8. `docs/04_PROJECT_STRUCTURE.md`
9. `docs/05_UI_UX_SPEC.md`
10. `docs/06_UI_DESIGN_SYSTEM.md`
11. `docs/18_SECURITY_RBAC_SPEC.md`
12. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
13. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
14. `docs/23_ERROR_HANDLING_SPEC.md`
15. `docs/27_SQLITE_SCHEMA_SPEC.md`
16. `docs/28_REST_API_CONTRACT.md`
17. `docs/29_TEST_STRATEGY.md`
18. `docs/30_ACCEPTANCE_CRITERIA.md`
19. `docs/31_IMPLEMENTATION_PROGRESS.md`
20. `docs/34_CODING_STANDARDS.md`
21. `docs/35_CONFIGURATION_SPEC.md`
22. `docs/37_SYSTEM_HEALTH_SPEC.md`
23. `docs/40_ANTI_CONTAMINATION.md`
24. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Then inspect all current foundation source and tests:

```text
backend/ipsp/**
frontend/**
database/migrations/**
tests/**
config/**
alembic.ini
pyproject.toml
requirements.lock
```

Before editing:

```text
git status --short
git rev-parse HEAD
git log -1 --oneline
```

Expected SHA:

```text
33a5901c67c706290c5f05087555dc315eff4cf4
```

Start from a clean tracked worktree except known user-owned prompt files.

---

# 4. Create the final acceptance artifact

Create:

```text
docs/PHASE_1_ACCEPTANCE_REPORT.md
```

This is an audit artifact, not a new frozen architecture specification.

It must contain:

- audited SHA;
- target release `v0.1.0`;
- audit date;
- Phase 1 scope;
- explicit boundary between foundation and later roadmap;
- complete Phase 1 acceptance matrix;
- V1 acceptance-criteria classification matrix;
- evidence references to implementation/tests;
- test/quality evidence;
- schema/migration/dependency state;
- security/privacy state;
- API inventory;
- unfinished-current-scope sweep;
- operational constraints;
- deferred capabilities;
- blockers, if any;
- release recommendation;
- next milestone as `v0.2 ingestion/storage/provenance — pending independent review` only.

Do not claim IPSP v1.0 is complete.

---

# 5. Phase 1 acceptance matrix

Audit every category below and give concrete source/test/runtime evidence.

## A. Repository / application foundation

Verify:

- Python 3.11+ contract;
- FastAPI app factory;
- runtime/package version remains `0.1.0`;
- canonical `/api/v1` root;
- static frontend root;
- centralized error handling;
- trace/request middleware;
- no static/API route shadowing;
- local-first runtime;
- no public-CDN production dependency.

## B. Configuration / secrets / outbound policy

Verify:

- typed settings;
- environment-aware safe validation;
- production fail-closed safety;
- SecretProvider abstraction;
- secret values are not ordinary persisted settings;
- deny-by-default outbound policy;
- feature flags cannot bypass outbound denial;
- Internet / remote LLM / model download / update-check controls;
- safe browser bootstrap exposes only necessary non-secret fields;
- foundation works with outbound disabled.

Remote provider implementation is not required in Phase 1.

## C. SQLite / migrations

Verify:

- synchronous SQLAlchemy 2.x;
- exactly one DeclarativeBase;
- exactly one Alembic history root;
- head exactly `20260812_05`;
- foreign keys enabled;
- no runtime `create_all` path;
- no async DB stack;
- safe behind-head/unmigrated behavior;
- migrated startup/readiness works.

Exactly seven Phase 1 application tables must exist:

```text
audit_events
jobs
permissions
role_permissions
roles
user_sessions
users
```

No eighth application table.

## D. User / Role / Permission schema

Verify:

- `users.role_id` gives one role per user;
- no persisted `is_admin`;
- RolePermission is sole permission mapping;
- canonical 13 permissions;
- frozen user fields/constraints;
- timezone-aware UTC behavior;
- no permission/role snapshot persisted in sessions.

Dataset ACL tables are later roadmap and must not be fabricated.

## E. Authentication / sessions

Verify:

- Argon2id;
- unknown/disabled/locked authentication privacy;
- failed-login tracking and lockout;
- opaque random sessions;
- only session-token hash stored;
- only CSRF hash stored;
- HttpOnly session cookie;
- Secure production cookies;
- SameSite;
- explicit localhost-development cookie exception;
- expiry;
- login rotation;
- logout invalidation;
- password-change invalidation;
- disabled-user session enforcement;
- required-password-change behavior;
- one-time first-admin bootstrap/CLI;
- no JWT/python-jose browser-auth architecture.

## F. CSRF

Verify state-changing browser foundation routes:

```text
POST /api/v1/auth/logout
POST /api/v1/auth/change-password
POST /api/v1/jobs/{job_id}/cancel
POST /api/v1/jobs/{job_id}/retry
```

Confirm missing/mismatch/cross-session rejection, stored-hash binding, GET routes being CSRF-free, and raw CSRF never being logged/returned. Frontend must read configured CSRF only at mutation time.

## G. RBAC

Verify:

- Role → RolePermission → Permission is sole authority;
- enforcement is server-side;
- role name `Admin` is not authority;
- non-Admin mapped permission can authorize;
- Admin-named role without mapping is denied;
- current DB authority is used rather than session snapshots;
- supported privilege changes invalidate sessions where required;
- catalog remains exactly 13 permissions.

Do not require a public user-management API if Phase 1 did not implement one.

## H. Observability / durable audit

Verify:

- structured rotating JSONL runtime logs;
- timestamp/event/trace/request IDs;
- non-secret `session_correlation_id`;
- authenticated user/resolved-role context where supplied;
- durable audit/security events in SQLite;
- runtime logs not treated as a full SQLite warehouse;
- auth/RBAC/job control audit events;
- safe exception diagnostics;
- literal-message logging guard;
- no password/hash/session/CSRF/Auth-header/API-key leak;
- request → runtime → audit correlation evidence.

## I. Persistent Job Service

Verify exact statuses:

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

Verify exact nine generic job types remain unchanged.

Verify:

- exactly one `jobs` table;
- persisted status/progress/error/artifacts;
- owner scoping;
- list/view/cancel/retry API;
- no public generic submit API;
- cooperative cancellation;
- retry;
- startup recovery;
- interrupted-job safe failure;
- bounded process-safe shutdown;
- permanently blocked handler cannot prevent process exit;
- stale/abandoned worker persistence authority is revoked;
- same-backend abandoned generation cannot overlap a new generation.

Keep the single-process LocalJobBackend constraint explicit. Redis/Celery/distributed workers remain future work.

## J. Health / operational diagnostics

Verify distinct surfaces:

```text
/health/live
/health/ready
/api/v1/admin/system/health
```

Liveness must be minimal/process-only.

Readiness must cover:

```text
application
configuration
database
foreign_keys
migration
runtime_logs
job_worker
```

Only `analytical_storage` remains deferred.

Admin health must remain permission-protected by `system.configure` and safely cover the Phase 1I rich diagnostic groups without remote network probes or secret/path/raw-error exposure.

Backup execution itself remains later roadmap; `never_run` is an acceptable current health state.

## K. Frontend foundation

Verify:

- HTML/CSS/Vanilla JS ES modules;
- no React/Vue/Angular/Svelte/Streamlit;
- no npm/build dependency;
- no CDN or remote font;
- CampaignSim / Powered by IPSP is branding only;
- canonical visual language preserved;
- no marketing-demo behavior copied;
- complete dark/light semantic themes;
- System/Dark/Light preference;
- only theme preference in localStorage;
- identity in memory only;
- no session-token access;
- correct CSRF cookie boundary;
- safe DOM construction/no unsafe sinks;
- hash router;
- abort/generation route lifecycle;
- cleanup ownership;
- responsive desktop/mobile shell;
- accessibility foundation;
- print-safe Jobs/System Health;
- Login;
- required-password flow;
- Overview;
- Jobs;
- Profile;
- System Health;
- safe loading/empty/error/permission states;
- no fake dataset/model/simulation functionality.

Full metadata-driven product UI is later roadmap.

## L. Integration / security proof

Reconfirm Phase 1K evidence:

- unmigrated → safe not-ready;
- migrated → ready;
- repeated worker lifespan;
- bootstrap → login → APIs → jobs → health → logout;
- owner-hidden jobs;
- offline/no-network foundation operation;
- trace/request/audit correlation;
- runtime-log privacy markers;
- static containment/path traversal resistance;
- safe central error envelope;
- readiness 503 minimal special contract;
- Admin browser journey;
- denied System Health journey;
- required-password journey;
- desktop/mobile browser evidence.

## M. Architecture / anti-contamination

Verify:

- dataset-agnostic core;
- no fixed benchmark fields/KPIs/models/controls;
- no RdF/BF funnel logic in production core;
- no BF6 production logic;
- no fixed marketing simulation assumptions;
- no Streamlit;
- sync SQLAlchemy;
- no Redis/Celery;
- no duplicate ORM ownership;
- no duplicate Alembic tree;
- no role-name authorization;
- no unsafe runtime remote dependency;
- reference HTML contributes visual design only.

`CampaignSim` is allowed only as initial user-facing branding, not backend/domain behavior.

## N. Documentation / operational usability

Verify README accurately describes current foundation behavior and preserves:

- local development steps;
- localhost cookie-security warning;
- first-admin bootstrap;
- quality commands;
- LocalJobBackend single-process warning;
- local/offline behavior;
- future engines explicitly unimplemented.

The current README may still contain an earlier Phase 1J implementation-status line. Correct it only after every Phase 1 gate passes.

---

# 6. Classify every V1 acceptance criterion

Read `docs/30_ACCEPTANCE_CRITERIA.md` line-by-line.

In `docs/PHASE_1_ACCEPTANCE_REPORT.md`, include a matrix titled:

```text
V1 Acceptance Criteria — Phase 1 Classification
```

Every criterion in that file must appear exactly once and receive one of:

```text
PASS
DEFERRED_BY_ROADMAP
NOT_APPLICABLE
BLOCKED
```

Do not silently omit any criterion.

Typical current Phase 1 PASS items, where evidence supports them, include authentication, RolePermission authority, password hashing, sessions/CSRF/lockout, outbound denial, secret privacy, trace/audit foundations, jobs, liveness/readiness/Admin health, dark/light UI foundation, and no-CDN operation.

Typical `DEFERRED_BY_ROADMAP` items include dataset permissions, ingestion formats, multi-table metadata, semantic inference, capability discovery, predictive modelling, simulation, trust, dynamic dataset/simulation flow, run history/reproduction, immutable run references, PDF/Excel exports, and actual backup/restore execution.

---

# 7. Version-consistency audit

Expected foundation version:

```text
0.1.0
```

Check at minimum:

- `pyproject.toml`;
- package/application metadata where present;
- `/api/v1` response;
- README/progress wording.

Do not bump to `0.1.1` or `1.0.0`.

Do not tag the repository.

A documentation-only mismatch may be corrected after all technical gates pass. A runtime/package mismatch is a blocker.

---

# 8. API inventory audit

Enumerate actual registered Phase 1 routes from source/runtime and include a concise inventory in the acceptance report.

Expected current foundation includes:

```text
/
GET /api/v1
/health/live
/health/ready
/api/v1/auth/*
/api/v1/jobs/*
/api/v1/admin/system/health
```

Future route families documented in `docs/28_REST_API_CONTRACT.md` are reserved architecture/domain families and need not exist yet.

Verify:

- one owner per current route;
- no duplicate operation;
- no static shadowing;
- safe Pydantic response contracts;
- no direct ORM return.

---

# 9. Unfinished-current-scope sweep

Search production code for:

```text
TODO
FIXME
HACK
XXX
NotImplementedError
raise NotImplementedError
pass
placeholder
temporary
```

Classify relevant findings.

Future namespaces/features may legitimately be `not_implemented`, but no advertised/current Phase 1 path—authentication, RBAC, jobs, health, current frontend, configuration, database, audit—may contain a real unfinished placeholder.

Record the result in the acceptance report.

---

# 10. Security/privacy acceptance sweep

Retain/re-run existing marker-based protections.

No current API/log/audit/health/frontend response may expose:

- raw password;
- password hash;
- raw session token;
- raw CSRF;
- Authorization header;
- API key/secret;
- DB URL;
- absolute local path;
- raw exception;
- SQL;
- secret request body;
- raw critical-log metadata.

Do not add permanent secret fixtures.

---

# 11. Dependency / reproducibility audit

Verify:

```text
pyproject.toml unchanged by Phase 1L
requirements.lock consistent
pip check passes
```

No new dependency.

If practical, create a disposable temporary virtual environment outside persistent project state, install from `requirements.lock`, install the project with `--no-deps`, and verify import/app construction. Remove the environment afterward.

If this clean reinstall cannot run solely because network/package-index access is unavailable, report the evidence as environmentally unavailable rather than automatically failing the product, provided lock consistency and current-environment `pip check` are green.

A genuinely inconsistent/broken lock is a blocker.

Do not leave a temporary venv in the repo.

---

# 12. Mandatory test execution

Run full suite:

```text
pytest
```

Required baseline:

```text
0 failed
0 skipped
0 warnings
```

Then separately rerun the high-value Phase 1K proof modules:

```text
pytest tests/integration/test_phase1_foundation_e2e.py tests/security/test_phase1_security_boundaries.py
```

Also rerun the complete job lifecycle integration file:

```text
pytest tests/integration/test_job_lifecycle.py
```

Do not use rerun-until-green loops or arbitrary sleep-based stabilization.

A reproducibly flaky foundation blocks Phase 1L.

---

# 13. Final browser acceptance

If the same browser QA facility used in Phase 1J/1K is available, perform a final acceptance pass against an isolated migrated DB.

Admin journey:

```text
open /
login
overview
jobs
profile
system health
System/Dark/Light theme
logout
```

Permission journey:

```text
ordinary authenticated user
#/admin/system
permission state
```

Required-password journey:

```text
must_change_password user
login
normal navigation blocked
change password or sign out path works
```

Responsive checks:

- desktop;
- about 390px mobile.

Confirm:

- no horizontal overflow;
- no console warning/error;
- no external runtime asset request;
- only theme preference in localStorage;
- session cookie unavailable to JS;
- no stale-route overwrite;
- System theme follows OS;
- valid readiness `not_ready` remains distinguishable from unreachable where exercised.

Do not add Playwright/Selenium/npm project dependencies.

If browser QA facility is unavailable, say so explicitly and rely on deterministic browser/source contracts plus Phase 1K evidence.

---

# 14. Quality gates

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

Run isolated Alembic verification:

```text
alembic heads
alembic current
alembic check
```

Use only an isolated temporary database if needed.

Expected:

```text
Alembic head: 20260812_05
Application ORM tables: exactly 7
```

Never intentionally migrate the default developer DB.

---

# 15. Repository hygiene

Before final report ensure no unintended residue remains:

- test DB;
- WAL/SHM;
- runtime JSONL/logs;
- browser profile;
- screenshot unless deliberately retained;
- marker file;
- archive;
- process/thread dump;
- node_modules/dist;
- npm lock/package file;
- temporary venv;
- credential/token/cookie dump.

Preserve user-owned prompts and intended audit documents/tests.

Run:

```text
git status --short
git diff --check
```

---

# 16. Intentional v0.1.0 boundaries

If Phase 1 passes, explicitly document these as roadmap boundaries rather than defects:

1. SQLite/local-first control plane.
2. LocalJobBackend is single-process only.
3. No Redis/Celery/distributed workers.
4. Analytical storage remains deferred.
5. No dataset ingestion yet.
6. No data-understanding/semantic engine yet.
7. No capability/model/simulation/trust engines yet.
8. Local/remote LLM providers not implemented.
9. Backup/restore execution not implemented.
10. PDF/Excel export not implemented.
11. Full metadata-driven dataset/simulation UI not implemented.
12. No public user-management workflow unless already implemented.
13. No dataset ACL enforcement because the dataset subsystem does not yet exist.

---

# 17. Documentation updates on PASS

Only after all gates pass:

## README.md

Update the implementation status so it clearly states that:

```text
Phase 1 / v0.1.0 foundation is complete/accepted pending independent final review of Phase 1L
```

Also identify the next implementation milestone as:

```text
v0.2.0 — ingestion/storage/provenance
```

but do not say it has started or is authorized.

Preserve explicit statements that ingestion, profiling, semantics, models, simulation, reports, and LLM execution are not implemented yet.

Do not call IPSP v1.0 production complete.

## docs/31_IMPLEMENTATION_PROGRESS.md

Add:

```text
Phase 1L — Final Phase 1 Acceptance Audit
```

If PASS, update the Phase 1 milestone to wording equivalent to:

```text
PHASE 1 COMPLETE — v0.1.0 foundation accepted pending independent final review
```

Do not mark v0.2 started or authorized.

---

# 18. Documentation behavior on FAIL

If any Phase 1 blocker is found:

- create/update the acceptance report with the blocker;
- leave README as Phase 1 in progress;
- leave implementation progress as Phase 1 in progress;
- mark Phase 1L FAIL;
- state v0.2 blocked;
- do not misclassify a current Phase 1 defect as deferred roadmap work.

---

# 19. Expected PASS diff boundary

A clean PASS should contain no changes under:

```text
backend/ipsp/
frontend/
database/migrations/
```

and no dependency changes.

If production code must change, Phase 1L must FAIL and stop.

Do not add large redundant test suites solely to increase the test count.

---

# 20. Mandatory Codex final report

Return every section.

## A. Starting state
SHA, branch, initial git status.

## B. Files created
Every retained file.

## C. Files modified
Every file.

## D. Audit methodology
Explain how specs, source, tests, runtime evidence and acceptance criteria were reconciled.

## E. Phase 1 acceptance matrix
Give PASS/BLOCKED summary for:

- application foundation;
- config/secrets/outbound;
- DB/migrations;
- user/role/permission schema;
- auth/session;
- CSRF;
- RBAC;
- observability/audit;
- jobs;
- health;
- frontend;
- integration/security;
- architecture/anti-contamination;
- documentation.

## F. V1 criteria classification
Give exact counts of:

- PASS
- DEFERRED_BY_ROADMAP
- NOT_APPLICABLE
- BLOCKED

Confirm every criterion from `docs/30_ACCEPTANCE_CRITERIA.md` appears in the acceptance report.

## G. Version consistency
List checked version surfaces and result.

## H. API inventory
List actual Phase 1 route families and duplicate/shadowing result.

## I. Unfinished-current-scope sweep
Report relevant TODO/FIXME/NotImplemented/pass/placeholder findings.

## J. Security/privacy
Report auth/session/CSRF/RBAC and marker/privacy result.

## K. Database/migration
Report head, exact table count, FK, DeclarativeBase, Alembic root, sync DB, no drift.

## L. Jobs
Report lifecycle, recovery, shutdown, authority, owner/API evidence.

## M. Observability/audit
Report trace/request/session correlation and redaction.

## N. Health
Report live/ready/Admin separation and privacy.

## O. Frontend/browser
Report final browser acceptance if available and static/security/theme/router evidence.

## P. Dependencies/reproducibility
Report lock audit, pip check, and disposable clean-install evidence if attempted.

## Q. Operational constraints
List intentional v0.1.0 boundaries.

## R. Production defects found
Expected on PASS:

`None`

Any production defect means Phase 1L FAIL.

## S. Production source changes
Expected on PASS:

`None`

## T. Prior-phase regression
Confirm Phase 1A through Phase 1K remain green.

## U. Tests
Report exact:

- full suite passed/failed/skipped/warnings/duration;
- focused Phase 1K rerun;
- job lifecycle rerun.

## V. Quality gates
Report compileall, Ruff lint/format, strict mypy, pip check, diff check, Alembic heads/current/check, browser acceptance, clean install if attempted.

## W. Schema/dependency state
Confirm pyproject, lock, migrations, ORM schema and npm/package state.

## X. Acceptance report
Confirm:

```text
docs/PHASE_1_ACCEPTANCE_REPORT.md
```

and summarize contents.

## Y. Documentation status
Report exact final README/progress status wording.

## Z. Repository/runtime residue
Report final hygiene check.

## AA. Phase boundary
Confirm Phase 1L only, v0.2 not started, and no Git tag/release created.

## AB. Deviations / unresolved issues
If none:

`None`

## AC. Gate result

End exactly with one:

`Phase 1L: PASS — v0.1.0 foundation ready for independent final acceptance; v0.2 remains blocked`

or

`Phase 1L: FAIL — v0.1.0 foundation not accepted; v0.2 blocked`

Do not begin v0.2.
