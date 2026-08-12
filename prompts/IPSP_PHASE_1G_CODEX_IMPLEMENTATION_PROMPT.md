# IPSP v1.0 — Phase 1G Codex Implementation Prompt
## Structured Observability, Durable Audit/Security Events & Safe Internal Diagnostics

**Repository:** `Kedar-Joshi07/IPSP`
**Required starting point:** `77d9d7d561dee1bc50bb80e471afb254ad470b7e`

Reviewed state:
- Phase 0 / 0.5: PASS
- Phase 1A / 1A.1: PASS
- Phase 1B: PASS
- Phase 1C / 1C.1: PASS
- Phase 1D: PASS
- Phase 1E / 1E.1: PASS
- Phase 1F / 1F.1: PASS
- Phase 1G: AUTHORIZED
- App version remains `v0.1.0`

This task is **Phase 1G only**. Do not begin Phase 1H jobs, Phase 1I rich Admin health, Phase 1J frontend expansion, or later ingestion/ML/LLM/simulation work.

# 1. Frozen observability contract

Every structured event supports:

```text
timestamp_utc
event_id
trace_id
request_id
component
action
status
severity
sanitized metadata
```

When context exists, include:

```text
session_correlation_id
user_id
resolved_role
duration_ms
error_code
resource_type
resource_id
project_id
dataset_id
dataset_version_id
semantic_version_id
capability_version_id
model_id
model_version_id
run_id
llm_provider
llm_model
llm_request_id
```

`session_correlation_id` is non-secret and must never be the bearer token/cookie.

Frozen logical streams:

```text
Audit
Security
Application
Frontend
Data Processing
ML
LLM
Simulation
Performance
Export
Errors
System
```

Durability split:

```text
Audit/Security -> may persist in SQLite
High-volume Application/Frontend/Performance/runtime -> structured rotating file sink
```

SQLite must not become the full runtime log warehouse.

Never log plaintext passwords, password hashes, API keys, raw session/CSRF tokens, cookies, Authorization headers, secret material, complete sensitive prompts, unrestricted sensitive rows, raw request bodies, or stack local-variable contents.

API/UI errors remain safe; internal logs may contain useful exception type + safe stack structure only.

# 2. Mandatory carried Phase 1A.1 item

Current `JsonFormatter` records only `exception_type`.

Phase 1G must add useful bounded structured stack/frame diagnostics without serializing:

- exception messages/args;
- traceback text;
- source-line text;
- local variables;
- object reprs from locals;
- absolute filesystem paths;
- environment values;
- secrets/raw sensitive data.

This is a required Phase 1G gate item.

# 3. Read before editing

Read:
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/00_SCOPE_FREEZE.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `docs/40_ANTI_CONTAMINATION.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Inspect:
- `backend/ipsp/observability/logging.py`
- `backend/ipsp/observability/context.py`
- `backend/ipsp/security/redaction.py`
- `backend/ipsp/errors/handlers.py`
- `backend/ipsp/auth/service.py`
- `backend/ipsp/auth/rbac.py`
- `backend/ipsp/api/dependencies/auth.py`
- `backend/ipsp/api/dependencies/rbac.py`
- `backend/ipsp/config/settings.py`
- `backend/ipsp/config/providers.py`
- `backend/ipsp/database/models/`
- `backend/ipsp/database/types.py`
- `backend/ipsp/database/migrations.py`
- `database/migrations/versions/20260811_03_phase1e_user_sessions.py`
- `tests/unit/test_logging.py`
- `tests/unit/test_redaction.py`
- `tests/integration/test_auth_api.py`
- `tests/integration/test_rbac.py`
- `tests/architecture/test_conformance.py`
- `tests/conftest.py`
- `pyproject.toml`
- `requirements.lock`

Run first:

```text
git status --short
git rev-parse HEAD
```

Preserve user-owned/untracked prompts.

# 4. Phase 1G objective

Implement:

1. canonical typed event-envelope/event-stream model;
2. request/trace/authenticated context propagation;
3. structured JSON runtime logs;
4. rotating local JSONL runtime sink;
5. safe structured exception frame diagnostics;
6. durable append-only `audit_events`;
7. one Alembic migration for `audit_events`;
8. `AuditEventRepository`;
9. `AuditService`;
10. durable selected auth/security/RBAC audit events;
11. atomic audit recording for security mutations where practical;
12. trace continuity tests;
13. strict runtime-log-vs-SQLite separation;
14. privacy/leak/conformance regressions.

No future domain event producers are required yet.

# 5. Out of scope

Do NOT implement:
- log-viewing REST API/Admin UI;
- frontend telemetry ingestion API;
- user/role management API;
- dataset ACL;
- jobs persistence/worker;
- Admin rich health;
- notifications/backups;
- external collectors/exporters;
- OpenTelemetry/Sentry/Splunk/Loki/Elasticsearch;
- Redis/Celery;
- async SQLAlchemy;
- remote telemetry/network logging;
- JWT;
- Streamlit;
- React/Vue/Angular;
- ML/LLM/simulation implementations.

No new observability package is expected.

# 6. Canonical event model

Create cohesive code under `backend/ipsp/observability/`, preferably:

```text
events.py
audit.py
logging.py
context.py
```

Create a typed stream enum with exactly these persisted/runtime values:

```text
audit
security
application
frontend
data_processing
ml
llm
simulation
performance
export
errors
system
```

Create one canonical event/envelope type/factory shared semantically by runtime logging and audit persistence.

Required:
- UUID-style unpredictable event ID;
- aware UTC timestamp;
- non-empty trace/request IDs;
- optional frozen context fields;
- sanitized metadata.

For non-HTTP CLI/service events, generate safe non-secret trace/request IDs when none exist.

# 7. Context propagation

Extend current context handling for:

```text
request_id
trace_id
session_correlation_id
user_id
resolved_role
```

Requirements:
- current safe request/trace validation remains;
- bind identity only after successful session authentication;
- use the existing non-secret session correlation ID;
- raw bearer/CSRF/cookie values never enter context;
- request state remains populated;
- context resets at request end;
- no cross-request leakage.

Because `BaseHTTPMiddleware` may not receive downstream ContextVar mutation back into the parent task, request-completion logging may read safe identity values from `request.state`.

# 8. Request completion event

Emit one minimal structured request-completion event with:

```text
stream = performance or application
component = api
action = http.request
status
duration_ms
metadata.method
metadata.path
metadata.status_code
```

Authenticated requests also include user ID, session correlation ID, and resolved role.

Never log query strings, bodies, cookies, auth/CSRF headers, response bodies, or arbitrary headers.

Preserve response `X-Request-ID` and `X-Trace-ID`.

# 9. Safe exception diagnostics

When `record.exc_info` exists, JSON may contain:

```text
exception_type
exception_frames
```

Each frame can contain only:

```text
file_name   # basename only
function
line_number
```

Requirements:
- bounded, max 32 frames;
- no exception message/args;
- no `traceback.format_exc()` output;
- no locals;
- no source-line text;
- no absolute paths;
- no environment values;
- no object reprs;
- no cause/context messages.

Tests must put secret markers in exception message, args, locals, and absolute path-like values and prove they are absent while safe frame structure remains.

# 10. Runtime rotating JSONL sink

Use stdlib only.

Extend `configure_logging(...)` to configure IPSP-managed:

1. structured console/stream handler;
2. `RotatingFileHandler` writing:

```text
<Settings.log_dir>/ipsp-runtime.jsonl
```

Recommended defaults:
- 10 MiB max;
- 5 backups;
- UTF-8.

Requirements:
- create log_dir safely;
- every file line valid JSON;
- same formatter;
- rotation tested;
- no duplicate handlers across repeated `create_app()`;
- reconfiguration closes only IPSP-owned old handlers;
- new test log_dir does not keep writing to an old one;
- unrelated root handlers untouched;
- no network sink.

Use existing `Settings.log_level` and `Settings.log_dir`. Do not add public config only for test convenience.

# 11. Runtime message safety

Variable runtime values belong in sanitized metadata/context.

Production IPSP logger calls should use developer-controlled static message strings. Avoid f-string/format interpolation of arbitrary runtime/user values into the message argument.

Add a reasonable architecture regression for IPSP production logger calls where practical.

# 12. `audit_events` ORM table

Phase 1G adds exactly one ORM table:

```text
audit_events
```

Expected ORM allowlist:

```text
audit_events
permissions
role_permissions
roles
user_sessions
users
```

Canonical ORM ownership stays under `backend/ipsp/database/models/`.

Preferred new model file:

```text
backend/ipsp/database/models/observability.py
```

# 13. Audit schema

Required minimum columns:

```text
id
event_id
timestamp_utc
stream
trace_id
request_id
session_correlation_id
user_id
resolved_role
component
action
status
severity
duration_ms
error_code
resource_type
resource_id
project_id
dataset_id
dataset_version_id
semantic_version_id
capability_version_id
model_id
model_version_id
run_id
llm_provider
llm_model
llm_request_id
metadata_json
```

Rules:
- integer PK;
- event_id unique/non-null;
- timestamp uses existing `UTCDateTime`;
- required envelope fields non-null;
- optional context nullable;
- duration >= 0 when present;
- metadata_json non-null;
- no raw session/CSRF/password/password-hash/token-hash/body/header columns;
- no FKs to future tables that do not yet exist.

Prefer historical scalar user_id rather than a destructive FK unless frozen docs explicitly require otherwise.

Index event ID, timestamp, trace ID, and user ID; add stream/action indexes only if useful. Do not over-index every future reference.

# 14. Append-only ownership

Audit rows are append-only through application ownership.

`AuditEventRepository` must not expose normal update/delete/overwrite operations.

No DB trigger is required now.

# 15. Metadata persistence

Before persistence:

```text
metadata
 -> sanitize_structured_data
 -> deterministic JSON
 -> metadata_json
```

Use deterministic compact JSON (`ensure_ascii=False`, `sort_keys=True`, compact separators).

Never persist Python repr; never use `eval`.

Provide safe decode helper for read/test/future use.

# 16. Audit repository/service

Create:

```text
backend/ipsp/repositories/audit.py
backend/ipsp/observability/audit.py
```

Repository:
- `add`
- `get_by_event_id`
- `list_recent` and/or `count` if useful
- sync SQLAlchemy 2.x
- receives Session
- never commits
- no BaseRepository
- no update/delete

AuditService:
- constructs canonical events;
- sanitizes metadata;
- supports `record(...)`;
- supports `record_in_session(...)` so security mutation + audit insert can share one transaction;
- no FastAPI types;
- no network;
- exposed through immutable `FoundationServices`.

Construct AuditService before Auth/RBAC and inject explicitly. Avoid circular imports and global service locators.

# 17. Current durable event coverage

Instrument at minimum:

### Security/auth
```text
auth.login
auth.logout
auth.password_change
auth.bootstrap_admin
auth.csrf_validation
```

### RBAC/governance
```text
rbac.permission_denied
rbac.user_role_change
rbac.role_permissions_change
rbac.catalog_sync
```

Do NOT audit every successful `has_permission()` or `/auth/me` request.

For mutations, insert the audit row in the same transaction where practical.

If durable audit insertion fails inside a security mutation transaction, the mutation must roll back; do not silently pretend audit succeeded.

# 18. Auth event privacy

Login success may contain:
- user_id;
- resolved role;
- session_correlation_id;
- trace/request IDs.

Login failure remains generic:
- do not persist attempted unknown username;
- do not encode public/account-state distinctions such as wrong/disabled/locked;
- no password/hash/token.

Keep Phase 1E.1 timing equalization unchanged.

Password-change and CSRF failure audit events must not store raw password/CSRF/session values.

# 19. Permission-denial audit

`enforce_permission()` denial may record:

```text
stream=security
action=rbac.permission_denied
status=failure
severity=WARNING
user_id
permission_code in sanitized metadata
```

When in HTTP context, include trace/request/session correlation/resolved role.

Public response remains only:

```text
403
AUTHZ-PERMISSION_DENIED
Permission denied.
trace_id
```

# 20. RBAC mutation audit

For role assignment, role mapping replacement, and catalog synchronization:

- audit actual privilege changes;
- preserve Phase 1F session invalidation semantics;
- no-op behavior must not claim a mutation occurred;
- either omit no-op mutation events or consistently mark `changed=false`, and test it.

# 21. Runtime error logging

Central error handlers should emit:

```text
stream=errors
component=api
action=exception.handled / exception.unexpected
status=failure
error_code
```

Handled domain errors stay safe.

Unexpected errors use `logger.exception(...)`; formatter emits only exception type + safe frames.

Never put `str(exc)` in output/metadata.

Client 500 body stays generic and contains no traceback.

# 22. Trace continuity

Add integration proof that one protected request can correlate:

```text
response X-Trace-ID / X-Request-ID
    =
runtime JSONL request event IDs
    =
durable security/audit event IDs for same request
```

For non-HTTP events, generated IDs only need to be valid/non-empty.

# 23. Runtime-vs-SQLite separation

Prove ordinary high-volume request logs do not create audit rows.

Health and ordinary `/auth/me` request completion should stay runtime-only.

Only explicitly selected security/audit actions persist to SQLite.

# 24. Alembic migration

Create exactly one migration, preferred:

```text
20260812_04
```

with parent:

```text
20260811_03
```

Migration:
- creates only `audit_events`;
- correct PK/unique/check/indexes;
- uses `UTCDateTime`;
- no seed rows;
- clean downgrade to 03;
- clean re-upgrade;
- `alembic check` passes;
- historical migrations untouched.

# 25. Migration/readiness tests

Isolated DB:

```text
empty -> 20260811_03 -> Phase1G head -> 20260811_03 -> Phase1G head
```

Verify:
- one Alembic head;
- only audit_events added;
- downgrade removes only audit_events;
- five prior tables remain;
- re-upgrade restores;
- `alembic check` clean;
- Phase1G head ready=200;
- DB at 20260811_03 => 503 `SYS-MIGRATION-REQUIRED`;
- liveness=200.

Never touch default DB.

# 26. Schema/persistence tests

Verify real SQLite:
- six-table allowlist;
- event_id uniqueness;
- required non-nullability;
- optional nullability;
- UTC round-trip;
- negative duration rejected;
- forbidden credential/body/header columns absent;
- sensitive metadata values redacted before persistence;
- raw audit-secret marker absent from SQLite text.

Repository has no normal update/delete API.

# 27. Auth/RBAC audit integration tests

Prove durable events for:
- login success/failure;
- logout;
- password-change success/failure;
- bootstrap admin;
- CSRF failure;
- permission denial;
- role assignment;
- role mapping change;
- catalog sync.

Also prove all prior session invalidation, lockout, CSRF, timing-equalization and anti-bypass tests remain green.

# 28. Exception privacy test

Raise an unexpected exception with markers in:
- exception message;
- exception arg;
- local variable;
- absolute temp path.

Parse structured log and prove:

Present:
- exception_type;
- safe frame file basename;
- function;
- line number.

Absent:
- message marker;
- arg marker;
- local marker;
- absolute path;
- source line;
- raw traceback text;
- `Traceback (most recent call last)`.

API 500 remains safe.

# 29. Runtime JSONL tests

With temp log_dir prove:
- app config creates JSONL sink;
- lines parse as JSON;
- required envelope fields exist;
- redaction works;
- repeated app creation does not duplicate handlers;
- reconfiguration closes/replaces old IPSP handler;
- rotation works with small test-specific limit/helper;
- backup count bounded;
- no files outside temp log_dir.

# 30. Redaction regression

Preserve deterministic exact/suffix key redaction.

Ensure current sensitive forms remain redacted, including at least:

```text
authorization
cookie
set_cookie
password
password_hash
session_token
csrf_token
access_token
refresh_token
api_key
secret
```

Do not introduce broad heuristics that destroy normal business metadata.

# 31. Architecture/conformance evolution

Expected model declaration ownership now includes:
- security model file;
- one canonical observability/audit model file.

Exact tables:

```text
audit_events
permissions
role_permissions
roles
user_sessions
users
```

Also prove:
- one DeclarativeBase;
- one Alembic root;
- one audit ORM definition;
- audit DB access only repository ownership;
- durable audit orchestration only observability/service ownership;
- no SQL in API routes/dependencies;
- no audit update/delete service;
- no runtime-log table;
- no permission snapshot in session;
- no persisted is_admin/role-name bypass;
- no Session.query;
- no async SQLAlchemy;
- no production create_all;
- no JWT/bcrypt/passlib;
- no Redis/Celery;
- no network log exporter;
- no Streamlit/React/Vue/Angular;
- no CDN;
- no benchmark contamination.

# 32. Dependency/config policy

No new dependency should be needed.

Use stdlib logging/RotatingFileHandler plus existing SQLAlchemy/Alembic.

Expected:
- `pyproject.toml` dependency list unchanged;
- `requirements.lock` unchanged;
- no clean dependency-regeneration venv.

Use existing `Settings.log_level` and `Settings.log_dir`.

Update `config/README.md` to document rotating JSONL and runtime-vs-audit durability.

# 33. Existing CLI safety

Preserve Phase 1F.1 `ipsp-sync-rbac` generic safe failure handling. Do not reintroduce traceback/raw operational details.

If RBAC sync now writes an audit row, CLI output must still show only safe counts.

# 34. Documentation

Update:
- `config/README.md`
- `database/migrations/README.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Record:

```text
Phase 1G — Structured Observability & Durable Audit
```

Document event envelope, streams, correlation, rotating runtime logs, audit_events, selected security/RBAC events, safe exception frames, runtime-vs-SQLite split, migration, and exact quality evidence.

Do not mark Phase 1/v0.1.0 complete.

# 35. Git discipline

Before/after:
```text
git status --short
git rev-parse HEAD
git diff --stat
git diff --check
```

Do not auto commit/push.

Do not track runtime logs/JSONL/rotations, DB/WAL/SHM, env files, secrets/tokens, venvs, caches, or archives.

Update `.gitignore` only if needed.

# 36. Quality gates

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

Migration smoke, isolated DB:

```text
alembic heads
alembic upgrade head
alembic current
alembic check
alembic downgrade 20260811_03
alembic upgrade head
```

# 37. Acceptance gate

PASS only if:
- canonical event envelope/stream set implemented;
- request/trace/auth context is isolated and correlated;
- rotating JSONL runtime sink works;
- safe stack diagnostics include structure but no message/locals/path/source/traceback text;
- exactly one new `audit_events` table and one migration;
- six-table allowlist;
- selected auth/RBAC events durable and sanitized;
- security mutation audit is atomic where applicable;
- ordinary request logs do not populate SQLite;
- Phase 1E/1F security behavior remains green;
- no dependency/network/framework/benchmark drift;
- all quality/migration gates pass.

# 38. Mandatory Codex final report

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Event model
Exact streams, envelope fields, ID/timestamp generation.

## E. Context propagation
Request, trace, user, session correlation, resolved role, reset/isolation.

## F. Runtime logging
Console + rotating JSONL path/rotation/reconfiguration.

## G. Safe exception diagnostics
Type, frame fields/count, excluded data, marker evidence.

## H. AuditEvent schema
All columns, PK/unique/index/check/nullability, forbidden-column absence.

## I. Migration
Revision/parent/upgrade/current/head/check/downgrade/re-upgrade/readiness.

## J. Audit repository/service
Ownership, transaction behavior, sanitization, append-only semantics.

## K. Auth/security audit integration
Login success/failure, logout, password change, bootstrap, CSRF failure.

## L. RBAC audit integration
Permission denial, role assignment, role mappings, catalog sync, session invalidation preservation.

## M. Trace continuity
Response IDs ↔ JSONL ↔ durable audit.

## N. Runtime-vs-SQLite separation
Evidence ordinary request logs do not create audit rows.

## O. Leak/privacy evidence
Password/hash/session/token/CSRF/cookie/header/exception/local/path/body markers absent.

## P. Authentication/RBAC regression
Phase 1E/1E.1/1F/1F.1 green.

## Q. Tests
Exact passed/failed/skipped/warnings.

## R. Quality gates
Compileall, Ruff lint/format, mypy, pip, diff check.

## S. Architecture/conformance
ORM allowlist, ownership, append-only audit, is_admin/role bypass, sync DB, no JWT/bcrypt/passlib, no Redis/Celery/network logging, no frameworks/CDN/contamination.

## T. Dependency state
pyproject dependency changes, requirements.lock changes, clean venv status.

## U. Runtime artifacts
Logs/JSONL/rotations, DB/WAL/SHM, secrets/tokens, venvs/caches.

## V. Git state
Final status + diff stat.

## W. Deviations / unresolved issues
If none: `None`

## X. Gate result

End exactly with one:

`Phase 1G: PASS — ready for independent review before Phase 1H`

or

`Phase 1G: FAIL — Phase 1H blocked`

Do not begin Phase 1H.
