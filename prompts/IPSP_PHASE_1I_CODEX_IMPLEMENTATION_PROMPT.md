# IPSP v1.0 — Phase 1I Codex Implementation Prompt
## Readiness Completion + Authorized Rich System Health Diagnostics

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `6b15fbe2ced7a555c72889891e918d042a0bbfe8`

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
- Phase 1I: AUTHORIZED
- Application version remains `v0.1.0`

This task is **Phase 1I only**.

Do not begin Phase 1J frontend/design-system expansion, ingestion, profiling, semantics, models, simulation, LLM providers, backup implementation, or later-domain work.

---

# 1. Frozen health architecture

Three different health surfaces are frozen and must remain distinct:

```text
/health/live
    -> unauthenticated infrastructure liveness
    -> process alive only
    -> minimal
    -> no dependency diagnostics

/health/ready
    -> unauthenticated infrastructure readiness
    -> required implemented dependencies only
    -> minimal safe statuses/error code
    -> 200 when ready, 503 when not ready

/api/v1/admin/system/health
    -> versioned application/Admin diagnostics
    -> server-side authorization
    -> sanitized rich diagnostics
```

The rich Admin health specification requires at minimum:

```text
SQLite connectivity/integrity status
Storage paths/free disk
Job worker health/queue depth
Local LLM configured/health
Remote LLM configured/reachable if policy allows test
Outbound internet policy state
Model artifact access
Last backup status
Recent critical errors
Memory/CPU summary where feasible
```

No health surface may leak secrets or sensitive raw diagnostics.

---

# 2. Read before editing

Read completely:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_PROJECT_STRUCTURE.md`
6. `docs/18_SECURITY_RBAC_SPEC.md`
7. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
8. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
9. `docs/23_ERROR_HANDLING_SPEC.md`
10. `docs/27_SQLITE_SCHEMA_SPEC.md`
11. `docs/28_REST_API_CONTRACT.md`
12. `docs/29_TEST_STRATEGY.md`
13. `docs/30_ACCEPTANCE_CRITERIA.md`
14. `docs/31_IMPLEMENTATION_PROGRESS.md`
15. `docs/34_CODING_STANDARDS.md`
16. `docs/35_CONFIGURATION_SPEC.md`
17. `docs/37_SYSTEM_HEALTH_SPEC.md`
18. `docs/40_ANTI_CONTAMINATION.md`
19. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Inspect current implementation, especially:

- `backend/ipsp/services/readiness.py`
- `backend/ipsp/api/routes/health.py`
- `backend/ipsp/api/schemas/common.py`
- `backend/ipsp/api/router.py`
- `backend/ipsp/api/routes/__init__.py`
- `backend/ipsp/api/dependencies/auth.py`
- `backend/ipsp/api/dependencies/rbac.py`
- `backend/ipsp/auth/rbac.py`
- `backend/ipsp/config/settings.py`
- `backend/ipsp/config/feature_flags.py`
- `backend/ipsp/config/providers.py`
- `backend/ipsp/security/outbound.py`
- `backend/ipsp/jobs/contracts.py`
- `backend/ipsp/jobs/local.py`
- `backend/ipsp/jobs/service.py`
- `backend/ipsp/repositories/jobs.py`
- `backend/ipsp/observability/logging.py`
- `backend/ipsp/observability/events.py`
- `backend/ipsp/main.py`
- `tests/conftest.py`
- `tests/integration/test_app.py`
- `tests/integration/test_job_lifecycle.py`
- `tests/architecture/test_conformance.py`
- `pyproject.toml`
- `requirements.lock`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Start from a clean tracked worktree except known user-owned prompt files.

---

# 3. Phase 1I objective

Implement:

1. completed runtime readiness now that the local job worker exists;
2. a separate startup/preflight readiness boundary so worker startup does not create a readiness cycle;
3. rich sanitized `SystemHealthService`;
4. `GET /api/v1/admin/system/health`;
5. server-side `system.configure` authorization;
6. SQLite connectivity + on-demand integrity diagnostics;
7. safe storage/free-space diagnostics;
8. job-worker/queue diagnostics;
9. honest LLM/provider health placeholders for features not implemented yet;
10. outbound-policy summary;
11. model-artifact storage access status;
12. latest backup-job status without implementing backup;
13. bounded recent-critical-error summaries from structured runtime logs;
14. CPU/memory summary where stdlib/platform support is feasible;
15. safe degraded/unavailable behavior for partial failures;
16. architecture/privacy/security regressions.

No schema or migration change is expected.

---

# 4. Explicitly out of scope

Do NOT implement:

- frontend/Admin health dashboard UI;
- `/logs` API;
- raw log browser;
- log download;
- local LLM provider;
- remote LLM provider;
- remote LLM API-key configuration;
- remote network reachability calls;
- Internet probe such as ping/http request;
- model registry;
- model loading;
- backup execution;
- restore execution;
- scheduler;
- email/Slack alerts;
- Prometheus;
- OpenTelemetry exporter;
- Sentry;
- Grafana;
- Redis/Celery;
- distributed worker health;
- analytics/data ingestion;
- user-management API;
- new permissions;
- database migration;
- new runtime dependency.

Phase 1J owns frontend work.

---

# 5. Authorization

The rich Admin health endpoint must use existing server-side RBAC.

Use:

```text
CorePermission.SYSTEM_CONFIGURE
```

because there is no frozen `system.view` or `health.view` permission.

Do **not** invent a new permission.

Do **not** authorize using:

```text
role_name == "Admin"
is_admin
superuser
```

Required behavior:

```text
unauthenticated                         -> 401
authenticated without system.configure -> 403
mapped non-Admin role with permission  -> 200
role name alone                         -> no authority
```

The endpoint is GET/read-only and does not require CSRF.

Do not require `logs.view` merely to receive the bounded critical-error summary inside system health. The endpoint returns only sanitized health summaries, not raw logs.

---

# 6. Readiness lifecycle: remove the job-worker deferral

The current readiness response still reports:

```text
deferred_checks:
    analytical_storage
    job_worker
```

The job worker now exists and must become a real runtime readiness dependency.

After Phase 1I:

```text
job_worker
    -> active readiness check
```

`analytical_storage` remains deferred because ingestion/Parquet analytical storage is not implemented yet.

Do not falsely declare future data/model/LLM systems ready.

---

# 7. Avoid the startup/readiness cycle

Current FastAPI lifespan checks readiness **before** starting the job backend.

If full readiness starts requiring a running job worker, this naïvely becomes:

```text
readiness requires worker
worker starts only when readiness passes
=> deadlock/not-ready forever
```

Refactor readiness into two explicit concepts.

Recommended API:

```text
ReadinessService.check_startup_preconditions()
    -> application/config/database/FK/migration + currently required pre-worker storage

ReadinessService.check()
    -> full runtime readiness
    -> startup preconditions
    -> job worker health
```

Exact method naming may differ.

Lifespan should use startup preconditions to decide whether it is safe to start the worker.

The public `/health/ready` must use **full runtime readiness**.

---

# 8. Job worker readiness

Use the existing sanitized:

```text
JobBackendHealth
running
accepting_jobs
worker_count
queue_depth
```

A worker is ready when it is running and accepting jobs.

If not:

```text
checks["job_worker"] = "not_ready"
error_code = "SYS-JOB-WORKER-NOT-READY"
HTTP /health/ready = 503
```

Do not require any registered domain handler for worker readiness. Production Phase 1H intentionally has zero domain handlers.

A worker with:

```text
running=True
accepting_jobs=True
```

is infrastructure-ready even if no domain handler is currently registered.

---

# 9. Worker startup failure must remain diagnosable

The purpose of liveness/readiness separation is that a process can be alive but not ready.

If startup preconditions pass but `job_backend.start()` fails with an expected safe operational failure:

- do not expose raw exception text;
- do not invent success;
- keep application process/routes available where possible;
- `/health/live` remains 200;
- `/health/ready` becomes 503 because job worker is not ready;
- authorized Admin health can report sanitized worker unavailability.

For unexpected worker-start exceptions, log safely with existing structured exception diagnostics.

Do not catch `KeyboardInterrupt`/`SystemExit`.

Use the threadpool boundary for synchronous worker lifecycle calls from async lifespan.

Also move job-backend shutdown through `run_in_threadpool(...)` so the async lifespan does not block the event loop during its bounded shutdown grace.

Do not run synchronous SQLAlchemy directly on the event loop.

---

# 10. Minimal public liveness must remain minimal

`GET /health/live` must remain:

```text
200
status=alive
timestamp
no rich checks
no storage
no DB details
no worker details
no policy
no LLM
no paths
no error history
```

Liveness must not fail because:

- database is unavailable;
- migration is stale;
- worker is stopped;
- disk health is degraded.

Its meaning is process/router alive only.

Add regression tests.

---

# 11. Minimal public readiness

`GET /health/ready` remains unauthenticated and minimal.

It may expose only safe status names such as:

```text
application
configuration
database
foreign_keys
migration
runtime_logs
job_worker
```

and:

```text
ready/not_ready
stable SYS-* error code
deferred_checks=["analytical_storage"]
```

Do not expose:

- DB URL;
- DB path;
- migration filesystem path;
- worker thread names;
- queue contents;
- job IDs;
- usernames;
- free disk bytes;
- LLM policy details;
- error-history details.

The rich endpoint owns those safe diagnostics.

---

# 12. Active storage in readiness

Do not pretend future analytical storage exists.

For Phase 1I public readiness, the only non-database storage dependency that is already active and required is the runtime structured-log directory/sink.

Add a minimal readiness check for runtime log storage:

```text
Settings.log_dir exists
is a directory
is readable/writable at the filesystem-policy level
```

Return only:

```text
checks["runtime_logs"] = "ready" / "not_ready"
```

Suggested stable failure code:

```text
SYS-STORAGE-UNAVAILABLE
```

Do not expose the path publicly.

`data_dir` and `artifacts_dir` may remain diagnostic/not-initialized until their functional phases.

Do not create arbitrary probe files from `/health/ready`.

---

# 13. SystemHealthService

Create a dedicated service, preferably:

```text
backend/ipsp/services/system_health.py
```

It is a synchronous service.

It must:

- contain no FastAPI types;
- perform no network calls;
- use explicit exception handling;
- never use bare `except:`;
- never return raw exception text;
- never return SQL;
- never return DB URLs;
- never return secret values;
- never return raw logs;
- never return full Settings/safe_snapshot;
- never mutate security/job/application state.

Expose it through immutable `FoundationServices`.

Do not create a mutable global health registry.

---

# 14. Typed internal/component states

Use a small typed status vocabulary.

Recommended overall states:

```text
healthy
degraded
unhealthy
```

Recommended component states may include:

```text
healthy
degraded
unhealthy
not_configured
not_implemented
not_available
not_initialized
never_run
```

Do not emit arbitrary exception-derived strings as statuses.

The overall status should be determined by **currently implemented required components**, not by future features that are not implemented/configured.

For example:

```text
local LLM not implemented
backup never run
model artifacts not initialized
```

must not by themselves make the whole application unhealthy in Phase 1I.

---

# 15. SQLite rich diagnostics

The authorized system health response should include safe SQLite diagnostics.

At minimum:

```text
status
connectivity
foreign_keys_enabled
migration_at_head
integrity_status
database_size_bytes if safely obtainable without path exposure
```

Use safe read-only SQL/PRAGMAs.

For integrity, use an on-demand SQLite integrity primitive such as:

```text
PRAGMA quick_check
```

This belongs in the rich authorized endpoint, **not** the high-frequency public readiness check.

Do not return raw integrity error strings. Map any non-`ok` result to a safe status such as:

```text
failed
```

Database size can be computed without revealing the DB path, e.g. SQLite page count × page size.

Catch:

```text
SQLAlchemyError
MigrationStateError
```

and return sanitized component state.

Do not expose table names or row contents in the health response.

---

# 16. Storage paths and free disk

Admin diagnostics must report the configured storage roles:

```text
data
artifacts
logs
```

For each provide safe operational fields such as:

```text
name
status
exists
is_directory
readable
writable
free_bytes
display_path
required_now
```

`display_path` must be sanitized.

Never return an absolute local path that can reveal:

```text
Windows username
home directory
drive-specific private layout
temporary-test root
repository parent
```

A safe approach is:

```text
path.name
or
repository-relative path when it can be safely derived
or
<external>/<basename>
```

Do not return `Settings.safe_snapshot()`.

If a future directory does not exist:

```text
data/artifacts -> not_initialized
```

is acceptable in Phase 1I.

The active log directory is required now.

Use `shutil.disk_usage`/stdlib filesystem APIs only.

Do not invent a low-disk threshold. Report free bytes; mark failure only when path/access/disk inspection itself is unavailable.

---

# 17. Job worker rich diagnostics

Use the existing backend health primitive.

Return at minimum:

```text
status
running
accepting_jobs
worker_count
queue_depth
```

It is also acceptable to include:

```text
persisted_queued_jobs
```

from `JobRepository.count_by_status(JobStatus.QUEUED)` if useful.

Do not expose:

- thread names;
- stack traces;
- queued job IDs;
- job metadata;
- owner usernames.

If DB inspection for persisted queue count fails, keep backend health available and safely mark the count unavailable.

---

# 18. Local LLM health must be honest

No local LLM provider exists yet.

The health response must **not** fabricate local model health.

It may report:

```text
feature_enabled = Settings.features.local_llm_enabled
configured = false / unknown
status = not_implemented
reachable = null
```

or an equivalent explicit contract.

Do not:

- import a model;
- download a model;
- load weights;
- scan arbitrary model directories;
- infer configured state from benchmark files.

Phase 0 architecture requires LLMs to be optional.

---

# 19. Remote LLM health must not perform network access

No remote LLM provider is implemented yet.

Report configuration/policy facts only.

Useful fields:

```text
feature_enabled
internet_enabled
remote_llm_policy_enabled
allowed_provider_count
configured
status
reachability_status
```

Do not return provider secrets.

Prefer not to return provider identifiers; a count is sufficient for Phase 1I.

Reachability:

```text
internet/policy disabled -> policy_disabled
provider layer absent     -> not_implemented
```

Do not perform:

```text
HTTP
DNS
ping
socket connect
provider API call
```

even if internet policy is enabled.

A real remote-provider reachability test belongs to the later provider phase.

---

# 20. Outbound policy summary

Return only safe non-secret policy state.

At minimum:

```text
internet_enabled
remote_llm_enabled
model_download_enabled
update_check_enabled
default_remote_transmission
allowed_remote_provider_count
```

Do not return secret values.

Do not mutate policy.

Do not bypass `OutboundPolicy`.

This is diagnostics only.

---

# 21. Model artifact access

The model registry is not implemented yet.

Report only the current configured artifact-storage condition:

```text
status
storage_accessible
display_path
```

If `artifacts_dir` does not exist:

```text
status=not_initialized
```

is acceptable.

Do not create model directories or model files merely to make health green.

Do not inspect future model formats.

---

# 22. Last backup status

Backup execution is not implemented, but `JobType.BACKUP` exists.

Report last backup from persisted job metadata if one exists.

Add a narrow repository read helper if needed, such as:

```text
get_latest_by_type(JobType.BACKUP)
```

Return only safe summary fields:

```text
status = never_run / queued / running / succeeded / failed / cancelled
job_id optional
updated_at/finished_at optional
safe error_code optional
```

Do not expose:

- error message if unnecessary;
- metadata;
- artifact paths;
- owner identity;
- raw exception.

If no backup job exists:

```text
status=never_run
```

This does **not** make overall health unhealthy in Phase 1I.

Do not implement a backup handler.

---

# 23. Recent critical errors

The frozen Admin health requires recent critical errors.

Use the existing structured runtime JSONL sink, not a new DB table.

Read only bounded recent structured log content.

Recommended policy:

```text
max files scanned: current + bounded rotated files
max entries returned: 10
severity == CRITICAL
```

Return only a safe summary shape such as:

```text
timestamp_utc
event_id
trace_id
component
action
error_code
```

Do not return:

- `message`;
- metadata;
- exception frames;
- exception type unless explicitly justified;
- stack/source;
- raw line;
- request body;
- paths;
- user data.

Malformed/non-JSON lines must be ignored safely.

If logs are unavailable:

```text
critical_error_status=not_available
```

Do not fail the entire admin health endpoint merely because history cannot be read.

Do not expose logs through `/health/ready`.

---

# 24. CPU and memory summary

Use standard library/platform-safe mechanisms only.

At minimum, where feasible:

```text
logical_cpu_count = os.cpu_count()
```

Optional values if safely and portably available:

```text
process_memory_bytes
load_average_1m
```

A metric unavailable on the current OS must be:

```text
null / not_available
```

rather than guessed.

Do not add `psutil`.

Do not expose process environment variables, command line, PID if not needed, usernames, hostnames, or filesystem paths.

---

# 25. Rich response schema

Create dedicated Pydantic response models, preferably under:

```text
backend/ipsp/api/schemas/system_health.py
```

Do not use free-form `dict[str, Any]` for the whole response.

Recommended top-level shape:

```text
status
timestamp_utc

readiness
database
storage[]
job_worker
local_llm
remote_llm
outbound_policy
model_artifacts
backup
recent_critical_errors
runtime
```

Exact nested model names may vary.

No ORM objects.

No raw Settings object.

No arbitrary exception strings.

---

# 26. Admin route

Create:

```text
backend/ipsp/api/routes/admin_system.py
```

or another single canonical route module.

Route:

```text
GET /api/v1/admin/system/health
```

Use:

```text
Depends(require_permission(CorePermission.SYSTEM_CONFIGURE))
```

or equivalent server-side dependency composition.

The route should be thin:

```text
authorize
get SystemHealthService
return mapped typed result
```

No direct SQL/disk/log parsing in route.

Register it through the single canonical `backend/ipsp/api/router.py`.

Do not add a second health route elsewhere.

---

# 27. Rich route HTTP behavior

For an authorized caller, prefer HTTP `200` with component states even when the application is degraded/unhealthy.

Reason:

```text
/health/ready
    -> machine readiness signal, 200/503

/admin/system/health
    -> diagnostic document explaining current state
```

Do not hide the diagnostic document behind a 503 merely because one component is unhealthy.

Authentication/authorization errors remain normal 401/403.

Unexpected internal route errors still use the central safe error envelope.

---

# 28. Privacy requirements

Add explicit marker tests.

No response from any health endpoint may contain:

```text
password
password_hash
session token
token hash
CSRF token
Authorization header
API key
secret
DB URL
absolute local path
Windows username/home path
raw exception message
SQL
request body
raw runtime log line
```

Use conspicuous markers such as:

```text
DO_NOT_LEAK_HEALTH_SECRET
DO_NOT_LEAK_HEALTH_DB_PATH
DO_NOT_LEAK_HEALTH_ERROR_MESSAGE
DO_NOT_LEAK_HEALTH_LOG_METADATA
```

Seed them only in isolated tests.

For the Admin route, even authorized access does not justify returning secrets/raw diagnostics.

---

# 29. Explicit error handling

Health checks must use explicit exception handling.

Allowed expected groups include:

```text
OSError
json.JSONDecodeError
SQLAlchemyError
MigrationStateError
```

plus narrow standard exceptions as needed.

No bare:

```python
except:
```

No:

```python
except Exception:
```

inside individual health probes merely to hide programming defects, unless it is the established outer central API boundary.

Do not put `str(exc)` into response fields or logs.

---

# 30. Readiness tests

Add/update integration tests proving:

### Healthy runtime
Inside active `TestClient` lifespan:

```text
/health/ready -> 200
checks include job_worker=ready
deferred_checks == ["analytical_storage"]
```

### Worker not running
Full readiness outside/after worker lifecycle:

```text
ready=false
job_worker=not_ready
SYS-JOB-WORKER-NOT-READY
```

### Migration stale
Database at prior migration state:

```text
/health/live -> 200
/health/ready -> 503
SYS-MIGRATION-REQUIRED
worker not started
```

### DB unavailable
Existing safe database readiness behavior remains.

### Runtime log storage unavailable
Readiness returns:

```text
503
SYS-STORAGE-UNAVAILABLE
```

without returning the path.

Use deterministic temp-path manipulation.

Do not make health tests depend on Internet.

---

# 31. Worker startup degradation test

Inject an expected backend-start failure without changing production semantics.

Prove:

```text
application lifespan remains available
/health/live = 200
/health/ready = 503
job_worker = not_ready
authorized Admin health reports unavailable worker safely
```

Do not leak injected marker text.

If the current FastAPI lifespan architecture makes this test cleaner using a narrow injected/stub backend, do so without adding a production global hook.

---

# 32. Public-vs-Admin separation tests

Assert public health responses contain none of:

```text
free_bytes
database_size_bytes
integrity_status
queue_depth
outbound
llm
backup
critical
display_path
memory
cpu
```

Then verify those diagnostics exist only in the authorized Admin route as appropriate.

This is an architecture/security boundary.

---

# 33. Admin authorization tests

Mandatory:

```text
GET admin health unauthenticated -> 401
User role without permission     -> 403
mapped non-Admin role            -> 200
```

Also demonstrate that a role merely named `Admin` without the `system.configure` mapping would not be authorized if practical using existing Phase 1F test helpers/patterns.

Do not weaken existing RBAC catalog behavior.

---

# 34. SQLite diagnostics tests

Using isolated SQLite:

- connectivity healthy;
- foreign keys enabled;
- migration at head;
- quick_check maps `ok` safely;
- database size is non-negative;
- injected SQLAlchemy/migration failure returns safe component state;
- raw DB URL/path/error marker absent from response.

Do not corrupt a real/default database.

If testing failed integrity directly is unsafe/flaky, inject the narrow probe result at service boundary rather than physically corrupting SQLite.

---

# 35. Storage diagnostics tests

Use temp directories.

Prove:

- logs current/required and healthy;
- data/artifacts may report not_initialized when absent;
- free bytes non-negative when available;
- absolute temp root does not appear in JSON;
- path display remains sanitized;
- inaccessible/non-directory condition maps safely.

Do not rely on Unix-only chmod behavior for Windows tests. Prefer deterministic path-shape cases such as a regular file where a directory is expected.

---

# 36. Critical-error summary tests

Seed isolated runtime JSONL with:

1. safe CRITICAL event;
2. INFO event;
3. malformed JSON;
4. CRITICAL event containing secret markers in message/metadata/path-like values.

Verify:

- only CRITICAL events are summarized;
- maximum entry count enforced;
- safe fields preserved;
- message/metadata/raw line excluded;
- secret/path markers absent;
- malformed lines ignored;
- public readiness/liveness do not expose the list.

---

# 37. Backup status tests

Persist representative `JobType.BACKUP` records.

Verify:

```text
none -> never_run
latest failed -> failed + safe error_code
latest succeeded -> succeeded
```

Latest is determined deterministically by timestamps/ID ordering.

Do not implement backup execution.

Do not expose backup job metadata/artifact refs.

---

# 38. LLM/outbound diagnostics tests

Test at least:

### Safe defaults
```text
local_llm feature false
remote_llm feature false
internet false
remote reachability policy_disabled/not_implemented
```

### Feature/policy enabled
Construct isolated Settings with safe non-secret provider identifiers.

Verify:
- status remains honest because provider implementation is absent;
- no network tool/library is called;
- only provider count is returned;
- no provider secret/name is required in response;
- no API key is exposed.

Do not add provider code.

---

# 39. Runtime metrics tests

Verify:

```text
logical_cpu_count is None or positive integer
```

Other unavailable metrics may be null.

Do not make OS-specific metrics mandatory across Windows/Linux/macOS.

---

# 40. Architecture/conformance evolution

Add/strengthen architecture tests proving:

- `/health/live` route remains only unversioned liveness;
- `/health/ready` remains only unversioned readiness;
- `/api/v1/admin/system/health` exists only under canonical Admin system route;
- Admin route uses `SYSTEM_CONFIGURE`, not role-name logic;
- rich health logic lives in service layer;
- routes contain no SQL;
- no raw Settings snapshot returned;
- no network client/import introduced for health;
- no `psutil`;
- no bare exception handlers in health implementation;
- no new ORM model/table;
- exact seven-table allowlist unchanged;
- one Alembic head remains `20260812_05`;
- no Redis/Celery;
- no async SQLAlchemy;
- no Streamlit;
- no React/Vue/Angular;
- no CDN;
- no benchmark contamination;
- static log-message guard remains green.

---

# 41. Schema/migration/dependency lock

Phase 1I is not a persistence-schema phase.

Expected:

```text
Alembic head = 20260812_05
ORM table allowlist = 7
no migration file
pyproject.toml unchanged
requirements.lock unchanged
```

Do not add `psutil` or any health library.

Do not regenerate dependency lock.

Do not create a clean dependency-resolution venv.

---

# 42. Documentation

Update:

- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `README.md` only if the public/Admin health distinction needs a concise operational note
- `config/README.md` only if behavior materially affects configuration

Record:

```text
Phase 1I — Readiness & Authorized System Health
```

Document:

- distinct liveness/readiness/Admin health roles;
- job worker is now an active readiness dependency;
- analytical_storage remains deferred;
- startup-precondition vs runtime-readiness split;
- rich Admin diagnostics;
- `system.configure` permission;
- safe path display;
- no remote reachability network call yet;
- no LLM/model/backup implementation;
- no schema/dependency changes;
- exact tests/quality evidence.

Do not mark Phase 1 complete.

Phase 1J remains next.

---

# 43. Git discipline

Before and after:

```text
git status --short
git rev-parse HEAD
git diff --stat
git diff --check
```

Do not automatically commit/push.

Do not track:

- runtime JSONL/log files;
- DB/WAL/SHM;
- health probe output dumps;
- temp dirs;
- secrets/tokens;
- venvs/caches;
- archives.

Preserve user-owned prompt files.

---

# 44. Quality gates

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

Also:

```text
alembic heads
alembic current
alembic check
```

Use isolated temp DB for migration/readiness tests.

Never mutate the default developer DB.

---

# 45. Phase 1I acceptance gate

PASS only if all are true.

### Separation
- liveness minimal and unauthenticated;
- readiness minimal and unauthenticated;
- Admin diagnostics rich and authorized;
- public probes never leak rich details.

### Readiness
- startup preconditions avoid worker cycle;
- job worker active check;
- runtime logs active storage check;
- analytical_storage still deferred;
- correct 200/503 behavior;
- worker startup failure produces alive-but-not-ready behavior.

### Admin diagnostics
- SQLite connectivity/integrity;
- sanitized storage/free disk;
- worker/queue;
- honest local LLM;
- honest remote LLM without network;
- outbound policy summary;
- model artifact access;
- latest backup job status;
- bounded critical-error summary;
- feasible runtime CPU/memory metrics.

### Authorization/privacy
- system.configure only;
- no role-name bypass;
- no secrets/raw tokens;
- no DB URL/absolute path;
- no raw logs/errors/SQL;
- typed response schema.

### Architecture
- no DB schema change;
- no dependency change;
- no provider/network implementation;
- no Phase 1J;
- seven ORM tables;
- one Alembic head;
- existing Phase 1E–1H.2 security/job regressions green.

### Quality
- pytest green;
- Ruff green;
- strict mypy green;
- compileall green;
- pip check green;
- diff check green;
- Alembic check green;
- docs accurate.

---

# 46. Mandatory Codex final report

Return every section.

## A. Starting state
- starting SHA
- branch
- initial git status

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Health architecture
Explain exact separation between:
- liveness
- readiness
- Admin system health

## E. Startup/readiness split
Report:
- startup-precondition checks
- full runtime checks
- how worker startup cycle is avoided
- worker-start failure behavior

## F. Public readiness
Report:
- exact check names
- active job worker semantics
- runtime log storage semantics
- deferred checks
- stable error codes

## G. Admin authorization
Report:
- permission used
- 401/403/200 tests
- proof role name is not authority

## H. SQLite diagnostics
Report:
- connectivity
- FK
- migration
- integrity
- size
- safe failure behavior

## I. Storage diagnostics
Report:
- data/artifacts/logs
- required_now
- free disk
- safe display-path policy
- missing/inaccessible behavior

## J. Job worker diagnostics
Report:
- running
- accepting
- workers
- queue depth
- persisted queue count if implemented

## K. LLM diagnostics
Report:
- local feature/configured/health behavior
- remote feature/policy/reachability behavior
- explicit confirmation no network test/provider was added

## L. Outbound policy
Report exact safe fields exposed.

## M. Model artifact diagnostics
Report accessibility and not-initialized behavior.

## N. Backup diagnostics
Report no-job/latest success/latest failure behavior and fields exposed.

## O. Critical-error diagnostics
Report:
- source files/logs scanned
- bound
- severity filter
- safe fields
- malformed-line handling
- leak markers

## P. Runtime CPU/memory
Report portable metrics and unavailable-platform behavior.

## Q. Privacy evidence
Explicitly confirm absence of:
- passwords/hashes
- session/CSRF/tokens
- auth headers/API keys
- DB URL
- absolute paths
- raw exception messages
- SQL
- raw log lines/metadata
- request bodies

## R. Prior-phase regression
Confirm Phase 1E through 1H.2 remain green.

## S. Tests
Exact:
- passed
- failed
- skipped
- warnings

## T. Quality gates
- compileall
- Ruff lint
- Ruff format
- strict mypy
- pip check
- git diff check
- Alembic heads/current/check

## U. Architecture/conformance
Explicitly report:
- ORM allowlist
- migration head
- health route ownership
- authorization dependency
- route SQL
- network imports
- psutil
- bare except
- async DB
- Redis/Celery
- frontend/framework/CDN
- benchmark contamination
- static-message guard

## V. Dependency/schema state
State:
- pyproject changes
- lock changes
- migration changes
- clean dependency environment status

Expected: none.

## W. Runtime artifacts
Report DB/WAL/SHM, logs, health dumps, venvs/caches.

## X. Git state
Final status and diff stat.

## Y. Deviations / unresolved issues
If none:
`None`

## Z. Gate result

End exactly with one:

`Phase 1I: PASS — ready for independent review before Phase 1J`

or

`Phase 1I: FAIL — Phase 1J blocked`

Do not begin Phase 1J.
