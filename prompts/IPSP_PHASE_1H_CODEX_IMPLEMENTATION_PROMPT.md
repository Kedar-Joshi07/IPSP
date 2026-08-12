# IPSP v1.0 — Phase 1H Codex Implementation Prompt
## Persistent Job Metadata, Local Worker Backend, Progress / Cancellation / Retry & Generic Job API

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `6c7b84d30133f7ac4a53d735563e061bb5228ec7`

Current independently reviewed state:

- Phase 0 / 0.5: PASS
- Phase 1A / 1A.1: FINAL PASS
- Phase 1B: FINAL PASS
- Phase 1C / 1C.1: FINAL PASS
- Phase 1D: FINAL PASS
- Phase 1E / 1E.1: FINAL PASS
- Phase 1F / 1F.1: FINAL PASS
- Phase 1G / 1G.1: FINAL PASS
- Phase 1H: AUTHORIZED
- Application version remains `v0.1.0`

This task is **Phase 1H only**.

Do not begin Phase 1I rich system health, Phase 1J frontend expansion, ingestion, profiling, semantic, model, simulation, or LLM implementation.

---

# 1. Frozen job architecture

The frozen platform contract is local-first:

```text
JobService
    ↓
JobBackend
    ↓
local worker initially

JobRepository
    ↓
SQLite job metadata
```

Future distributed execution may introduce:

```text
Redis / Celery
```

only as a later provider. They are **not permitted in Phase 1H**.

The frozen concepts already present are:

```text
JobBackend
JobService
JobRepository
JobStatus
JobType
JobProgress
JobError
JobSnapshot
```

The current contracts are foundation stubs, not the final implementation.

Frozen lifecycle states:

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

Frozen dataset-agnostic job families:

```text
UPLOAD_PROCESSING
PROFILING
RELATIONSHIP_ANALYSIS
MODEL_TRAINING
SYNTHETIC_FITTING
SIMULATION
REPORT_GENERATION
BACKUP
RESTORE
```

Do not add marketing/domain-specific job types.

The SQLite schema specification requires foundation `jobs` metadata to record:

- job type/status;
- progress;
- owner;
- trace ID;
- timestamps;
- retryability;
- cancellation;
- artifact references;
- sanitized error details.

The REST contract contains `/api/v1/jobs` and requires async long-running endpoints to return job/run IDs and status links.

---

# 2. Read before editing

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
10. `docs/28_REST_API_CONTRACT.md`
11. `docs/29_TEST_STRATEGY.md`
12. `docs/30_ACCEPTANCE_CRITERIA.md`
13. `docs/31_IMPLEMENTATION_PROGRESS.md`
14. `docs/34_CODING_STANDARDS.md`
15. `docs/37_SYSTEM_HEALTH_SPEC.md`
16. `docs/40_ANTI_CONTAMINATION.md`
17. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Inspect current implementation, especially:

- `backend/ipsp/jobs/contracts.py`
- `backend/ipsp/jobs/enums.py`
- `backend/ipsp/jobs/__init__.py`
- `backend/ipsp/config/providers.py`
- `backend/ipsp/database/models/`
- `backend/ipsp/database/session.py`
- `backend/ipsp/observability/audit.py`
- `backend/ipsp/observability/events.py`
- `backend/ipsp/observability/context.py`
- `backend/ipsp/api/dependencies/auth.py`
- `backend/ipsp/api/dependencies/rbac.py`
- `backend/ipsp/auth/rbac.py`
- `backend/ipsp/errors/exceptions.py`
- `backend/ipsp/errors/handlers.py`
- `backend/ipsp/services/readiness.py`
- `tests/architecture/test_conformance.py`
- `tests/integration/test_database_foundation.py`
- `tests/integration/test_observability.py`
- `tests/integration/test_rbac.py`
- `pyproject.toml`
- `requirements.lock`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Preserve user-owned prompt files.

---

# 3. Phase 1H objective

Implement the production foundation for long-running local jobs:

1. canonical persistent `jobs` ORM table;
2. one Alembic migration;
3. concrete synchronous `JobRepository`;
4. concrete `JobService`;
5. local in-process `JobBackend`;
6. handler-registration/execution contract;
7. progress reporting;
8. cooperative cancellation;
9. retry semantics;
10. safe error capture;
11. restart/recovery policy;
12. generic job status/list/cancel/retry API;
13. server-side authorization;
14. structured runtime logging;
15. durable selected job audit events;
16. worker readiness primitive for future Phase 1I;
17. comprehensive lifecycle/concurrency/privacy tests.

No domain-specific job implementation is required in this phase.

---

# 4. Explicitly out of scope

Do NOT implement:

- actual upload processing;
- profiling algorithms;
- relationship inference;
- model training;
- SDV fitting;
- simulation;
- report generation;
- backup/restore logic;
- Redis;
- Celery;
- RabbitMQ;
- Kafka;
- external queues;
- multiprocessing cluster;
- async SQLAlchemy;
- a scheduler/cron system;
- frontend job dashboard;
- websocket/SSE progress streaming;
- email/Slack notifications;
- Admin rich health endpoint;
- job prioritization;
- DAG/workflow orchestration;
- distributed locks;
- remote worker protocol;
- arbitrary Python-code submission;
- user-supplied callable/module imports;
- runtime network calls.

Phase 1H is generic infrastructure only.

---

# 5. Existing contract evolution

Do not create duplicate competing job abstractions.

Evolve the current:

```text
backend/ipsp/jobs/contracts.py
backend/ipsp/jobs/enums.py
```

into the canonical Phase 1H contracts.

Keep:

```text
JobStatus
JobType
JobProgress
JobError
JobSnapshot
JobBackend
JobRepository
JobService
```

unless a small cohesive split improves ownership.

If converting `JobService` / `JobRepository` from Protocol names into concrete classes would create naming ambiguity, use a clear pattern such as:

```text
JobRepository protocol -> JobRepositoryProtocol
concrete repository -> JobRepository
```

or remove obsolete protocols in favor of concrete ownership.

Do not leave two public classes with confusingly identical responsibility.

---

# 6. Job lifecycle/state machine

Use exactly the frozen statuses:

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

Allowed state transitions:

```text
QUEUED    -> RUNNING
QUEUED    -> CANCELLED

RUNNING   -> SUCCEEDED
RUNNING   -> FAILED
RUNNING   -> CANCELLED   # cooperative cancellation acknowledged

FAILED    -> QUEUED      # retry only when retryable
CANCELLED -> QUEUED      # retry only if policy permits
```

Terminal by default:

```text
SUCCEEDED
FAILED
CANCELLED
```

`SUCCEEDED` cannot be retried.

Reject all illegal transitions in the service/repository boundary.

No implicit transition from terminal state back to RUNNING.

Retry must create a new execution attempt on the **same logical job ID** only if this is consistent with frozen specs; otherwise create a new job ID linked to the prior job. Since current frozen contracts expose `retry(job_id)` and no parent-job field is frozen, prefer same logical job row with an incremented attempt counter unless source docs contradict this during implementation.

Do not invent extra public lifecycle states such as `PENDING`, `PAUSED`, `RETRYING`, `TIMED_OUT`, `ABORTED`.

---

# 7. Progress contract

Preserve:

```text
percent: 0..100
phase: str
message: str
```

Hardening requirements:

- percent integer in range 0–100;
- phase/message bounded;
- no multiline/unbounded text;
- progress text is developer-controlled or sanitized;
- no credentials/raw rows;
- progress updates are persisted;
- progress timestamp updates job `updated_at`;
- progress cannot move a terminal job back into active state;
- success ends at 100%;
- initial queued progress is 0%.

Do not require progress percentages to be strictly monotonic unless frozen docs require that. Some real operations may restart internal phases. The final succeeded snapshot must be 100%.

---

# 8. Safe job error contract

Preserve:

```text
error_code
message
retryable
```

Persist only safe errors.

Never persist:

- raw exception message;
- traceback;
- exception args;
- locals;
- SQL;
- DB URL;
- filesystem secrets;
- passwords;
- session/CSRF tokens;
- API keys;
- raw request body;
- arbitrary user rows.

When a handler raises an unexpected exception:

```text
runtime structured log:
    safe exception type + safe frames via existing Phase 1G logger

jobs row:
    stable safe JOB-* error code
    generic safe message
    retryable flag
```

Recommended unexpected worker error:

```text
JOB-EXECUTION-FAILED
Job execution failed.
```

Do not put `str(exc)` into DB or API.

---

# 9. `jobs` ORM schema

Add exactly one new production table:

```text
jobs
```

Expected ORM allowlist after Phase 1H:

```text
audit_events
jobs
permissions
role_permissions
roles
user_sessions
users
```

Canonical ORM ownership stays under:

```text
backend/ipsp/database/models/
```

Preferred new file:

```text
backend/ipsp/database/models/jobs.py
```

or another single cohesive canonical jobs model file.

No ORM classes under `backend/ipsp/jobs/`.

---

# 10. Required job columns

Implement the minimum persistent schema supporting the frozen contract.

Recommended columns:

```text
id                      integer PK
job_id                  unique non-null string UUID
job_type                non-null string
status                  non-null string

progress_percent        non-null integer
progress_phase          non-null string
progress_message        non-null string

owner_user_id           nullable integer
trace_id                non-null string
request_id              nullable string

attempt_count           non-null integer
max_attempts            non-null integer
retryable               non-null boolean
cancel_requested        non-null boolean

error_code              nullable string
error_message           nullable string

artifact_refs_json      non-null JSON-text string
metadata_json           non-null sanitized JSON-text string

created_at              non-null UTC
queued_at               non-null UTC
started_at              nullable UTC
finished_at             nullable UTC
updated_at              non-null UTC
```

If current frozen docs require a slightly different naming shape, follow them.

Rules:

- `job_id` server-generated UUID, never client chosen;
- progress 0–100 DB check;
- attempt_count >= 0/1 according to chosen semantics;
- max_attempts >= 1;
- artifact/metadata JSON deterministic and sanitized;
- `owner_user_id` may be an FK to `users.id` if deletion semantics are safe; otherwise a historical scalar is acceptable. Prefer consistency with current audit/history design.
- no payload blob containing arbitrary business data;
- no bearer/token/hash/cookie/password columns;
- no raw traceback/error-details column;
- no pickled Python objects;
- no callable/module path persisted for arbitrary execution.

Add only useful indexes:
- unique job_id;
- status;
- job_type;
- owner_user_id;
- created_at/updated_at where useful.

Do not over-index.

---

# 11. Artifact references

`artifact_refs_json` stores only references/identifiers/relative artifact locations that are safe to expose according to future policy.

Do not store artifact bytes in SQLite.

Do not store absolute sensitive filesystem paths.

Provide deterministic serialization and a safe decode helper.

Phase 1H test handlers may attach synthetic safe references such as:

```text
reports/example-id
models/example-id
```

but production job types remain generic.

---

# 12. Sanitized job metadata

`metadata_json` is for bounded, non-secret execution metadata/correlation only.

Use:

```text
sanitize_structured_data(...)
    ↓
deterministic JSON
```

Do not store arbitrary request payloads.

Recommended limits:
- bounded serialized length;
- reject or replace unsupported objects;
- exact credential key redaction from existing redactor;
- no `repr`.

Do not use `eval`/pickle.

---

# 13. Migration

Create exactly one new Alembic revision with parent:

```text
20260812_04
```

Preferred deterministic revision:

```text
20260812_05
```

unless repository conventions require another deterministic identifier.

Migration:

- creates only `jobs`;
- uses existing `UTCDateTime`;
- includes constraints/indexes;
- no job seed rows;
- downgrade drops only `jobs`;
- clean 04 -> 05 -> 04 -> 05 lifecycle;
- historical migrations untouched.

Expected new head:

```text
20260812_05
```

---

# 14. Concrete JobRepository

Create:

```text
backend/ipsp/repositories/jobs.py
```

Repository responsibilities may include:

```text
add
get_by_job_id
list_for_owner
list_recent
transition
update_progress
request_cancel
clear_cancel_request
mark_running
mark_succeeded
mark_failed
mark_cancelled
prepare_retry
count_by_status
```

Exact method split may vary.

Requirements:

- synchronous SQLAlchemy 2.x;
- caller supplies Session;
- no commit ownership;
- no `Session.query()`;
- no hidden async;
- atomic conditional state changes where concurrency matters;
- no generic BaseRepository;
- no business/domain execution logic in repository.

Avoid unsafe read-modify-write races for cancellation/claiming.

Where practical use guarded `UPDATE ... WHERE status IN (...)` and check row count.

---

# 15. Handler execution contract

Define a trusted internal handler interface, for example:

```python
JobHandler = Callable[[JobExecutionContext], None]
```

or Protocol.

`JobExecutionContext` should expose only safe infrastructure capabilities:

```text
job_id
job_type
attempt
update_progress(...)
is_cancel_requested()
raise_if_cancelled()
add_artifact_reference(...)
```

Potentially safe non-secret observability IDs are acceptable.

Do not pass SQLAlchemy Session into arbitrary handlers.

Do not let handlers mutate ORM rows directly.

Do not support dynamically importing handler paths from DB/user input.

Handlers are registered explicitly by trusted application composition:

```text
JobType -> handler callable
```

No handler is required for every frozen JobType in Phase 1H.

Submitting a job type with no registered handler must fail safely or remain queued according to an explicit policy. Prefer fail-fast submission with a stable safe `JOB-HANDLER-UNAVAILABLE` error rather than accepting work that can never execute.

---

# 16. Local JobBackend

Implement a local, in-process backend under:

```text
backend/ipsp/jobs/
```

Preferred name:

```text
LocalJobBackend
```

Use standard-library concurrency only, preferably:

```text
concurrent.futures.ThreadPoolExecutor
```

No external worker dependency.

Requirements:

- bounded worker count;
- no thread per job;
- start/stop lifecycle explicit;
- safe shutdown;
- no network;
- backend accepts only job IDs/types already persisted by JobService;
- handler registry immutable or safely synchronized after startup;
- no user-supplied callables;
- no arbitrary code execution;
- submit schedules execution asynchronously;
- cancel requests cooperative cancellation;
- retry requeues through JobService policy;
- exceptions never escape worker thread unhandled to corrupt process state.

Do not run SQLite sessions across threads. Every worker operation obtains its own session through `DatabaseSessionFactory`.

---

# 17. Worker ownership / circular dependency avoidance

Avoid:

```text
JobService -> JobBackend -> JobService -> ...
```

with uncontrolled circular construction.

A clean architecture is:

```text
JobService
  ├── creates/persists job
  ├── validates transitions/policy
  └── asks backend.enqueue(job_id)

LocalJobBackend
  └── invokes JobExecutor.execute(job_id)

JobExecutor
  ├── loads current job
  ├── claims QUEUED -> RUNNING atomically
  ├── calls trusted registered handler
  ├── persists progress/result/failure
  └── cooperatively observes cancellation
```

Exact classes may vary, but ownership must remain explicit/testable.

Do not use global mutable worker registries.

---

# 18. JobService

Implement a concrete application service.

Expected operations:

```text
submit(job_type, owner_user_id, ...)
get(job_id, requesting_user...)
list(...)
progress(job_id)
cancel(job_id)
retry(job_id)
```

Internal/admin forms may separate authorization from service; API authorization remains server-side.

The service must:

- generate job UUID;
- preserve active trace/request context;
- persist before enqueue;
- enforce legal transitions;
- return immutable snapshots;
- handle enqueue failure safely;
- support cancellation/retry;
- never leak ORM entities.

If enqueue fails after persistence, mark the job FAILED safely rather than leaving an orphaned QUEUED row indefinitely.

---

# 19. Retry semantics

Retry is allowed only if:

```text
status in {FAILED, CANCELLED}
AND retryable is true
AND attempt_count < max_attempts
```

`SUCCEEDED` cannot retry.

On retry:

- clear previous safe error;
- clear cancel_requested;
- progress resets to 0;
- status returns to QUEUED;
- queued_at/updated_at refresh;
- started_at/finished_at reset appropriately;
- attempt_count increments according to your documented semantics;
- enqueue exactly once.

Prevent double retry races.

If max attempts exhausted:

```text
JOB-RETRY-NOT-ALLOWED
```

safe client message.

Do not implement exponential delayed retries or auto-retry scheduling in Phase 1H unless frozen docs explicitly demand it.

Default should be **manual retry only**.

---

# 20. Cancellation semantics

Cancellation is cooperative.

### QUEUED
A cancel request should atomically move it directly to:

```text
CANCELLED
```

without executing the handler if not already claimed.

### RUNNING
Set:

```text
cancel_requested = true
```

The handler/executor must observe this through `JobExecutionContext`.

When acknowledged:

```text
RUNNING -> CANCELLED
```

Do not kill Python threads.

Do not pretend cancellation succeeded if a handler has already completed.

Cancellation must be idempotent where possible.

Public API should clearly distinguish:
- cancellation accepted;
- already terminal/no longer cancellable.

Do not expose thread IDs or worker internals.

---

# 21. Job startup/restart recovery

An in-process worker cannot survive process restart.

Define deterministic startup recovery.

At application startup after DB is migrated, do **not** silently execute stale domain jobs unless explicitly registered and safe.

Recommended local-first policy:

- persisted `QUEUED` jobs remain queued and can be explicitly recovered/enqueued by worker startup only if the relevant handler is registered;
- persisted `RUNNING` jobs from a previous process are no longer actually running and must not remain falsely RUNNING forever;
- mark stale prior-process RUNNING jobs as FAILED with a safe retryable error such as:

```text
JOB-WORKER-INTERRUPTED
Job execution was interrupted.
```

- make them manually retryable;
- record durable audit/runtime event;
- no automatic infinite retry.

To distinguish prior-process RUNNING jobs robustly, perform recovery once on explicit worker start.

Document and test this policy.

Do not invent distributed leases/heartbeats in Phase 1H.

---

# 22. App startup/shutdown integration

Integrate local worker lifecycle with FastAPI lifespan or another explicit application lifecycle mechanism.

Requirements:

- worker starts once per app instance;
- worker shuts down safely;
- repeated `TestClient` / `create_app()` usage does not leak worker threads;
- app construction itself does not execute jobs before lifespan/startup;
- no database migration at startup;
- migrations still remain explicit;
- if DB is below head, worker must not corrupt/create schema.

Do not replace current app factory with global application side effects.

If current testing architecture makes worker auto-start unsafe, an explicit lifecycle service can start only during lifespan.

---

# 23. Worker readiness primitive

Phase 1I will expose richer health.

Phase 1H should provide a sanitized primitive such as:

```text
JobBackendHealth
    running
    accepting_jobs
    worker_count
    queue_depth
```

or equivalent.

No Admin route yet.

Readiness integration in Phase 1H should be conservative:

- if the local job worker is a required active runtime dependency for normal long-running operations, include a minimal `job_worker` readiness check after startup;
- if adding it would change current infrastructure semantics beyond frozen docs, expose the health primitive and defer wiring to readiness until Phase 1I.

Do not invent rich diagnostics.

Whichever choice is made, document it and test it.

---

# 24. Job observability

Use existing Phase 1G structured event infrastructure.

Recommended runtime events:

```text
job.submitted
job.started
job.progress
job.succeeded
job.failed
job.cancel_requested
job.cancelled
job.retry_requested
job.recovered_interrupted
```

Streams:

```text
application / performance / errors
```

as appropriate.

Do not log progress on every tiny internal update if it creates excessive volume. Test handlers may update a few times.

Runtime logs must include:

```text
job_id
trace_id
user_id when available
duration_ms when meaningful
```

Use canonical resource context:

```text
resource_type = "job"
resource_id = job_id
```

Do not put job metadata into message strings.

Static-message AST policy from Phase 1G.1 must remain green.

---

# 25. Durable job audit events

Durably audit security/governance-relevant job control actions, not every progress tick.

At minimum:

```text
job.submit
job.cancel
job.retry
```

Use `EventStream.AUDIT` or `SECURITY` as appropriate.

The audit event should include:
- actor user ID when present;
- job ID;
- job type;
- safe status;
- trace/request correlation;
- no payload/secrets.

Worker execution lifecycle (`started/succeeded/failed`) may remain runtime structured logs unless frozen docs require durable audit. If you choose to durably audit terminal outcomes, keep write volume bounded and consistent.

Do not put all job logs in `audit_events`.

---

# 26. Generic `/api/v1/jobs` API

Implement only generic job-management routes under:

```text
backend/ipsp/api/routes/jobs.py
backend/ipsp/api/schemas/jobs.py
```

Recommended endpoints:

```text
GET  /api/v1/jobs
GET  /api/v1/jobs/{job_id}
POST /api/v1/jobs/{job_id}/cancel
POST /api/v1/jobs/{job_id}/retry
```

A generic public `POST /jobs` that lets clients choose arbitrary `JobType` is **not required** and should preferably be omitted in Phase 1H. Future domain endpoints will submit the correct job type through JobService.

If a test-only submit route is needed, attach it only in tests.

Response model should expose safe fields:

```text
job_id
job_type
status
progress
created_at
updated_at
started_at
finished_at
retryable
cancel_requested
attempt_count
max_attempts
safe error
safe artifact refs
links if useful
```

Do not expose internal metadata blindly.

---

# 27. Job authorization

There is no frozen standalone `job.*` permission code.

Do **not** invent one.

For v0.1 generic job routes:

- every route requires authentication;
- ordinary users may view/control only their own jobs;
- cross-owner access must fail closed;
- a user with `system.configure` may be allowed to inspect/control all jobs if needed for operational administration, but do not use role name `"Admin"` as authority;
- alternatively keep all generic routes owner-only until a dedicated permission is frozen.

Prefer the simpler **owner-only** policy in Phase 1H unless frozen docs explicitly require cross-user Admin access.

A job with `owner_user_id=None` should not be exposed to ordinary users.

Do not infer authority from `resolved_role`.

---

# 28. CSRF

State-changing browser routes:

```text
cancel
retry
```

must require:

```text
authenticated session
+
CSRF
```

GET routes require authentication but no CSRF.

Preserve 401 vs 403 behavior.

Do not put CSRF into JobService.

---

# 29. Job API errors

Use safe `JOB-*` errors through existing IPSP error envelope.

Recommended stable codes:

```text
JOB-NOT-FOUND
JOB-CANCEL-NOT-ALLOWED
JOB-RETRY-NOT-ALLOWED
JOB-HANDLER-UNAVAILABLE
JOB-EXECUTION-FAILED
JOB-WORKER-UNAVAILABLE
```

Do not reveal whether another user's job exists.

For owner lookup:

```text
not found
OR exists but different owner
    -> same JOB-NOT-FOUND public response
```

Avoid resource enumeration.

---

# 30. Handler registration

Production composition may initially register **zero domain handlers** because later phases own actual operations.

Tests can inject trusted handlers explicitly.

If zero handlers are registered:
- worker health may still be healthy/accepting infrastructure;
- generic GET job routes work;
- no arbitrary job submission endpoint exists.

Provide a clean method for later phases to register handlers during composition without editing core worker internals.

No plugin dynamic import in Phase 1H.

---

# 31. FoundationServices composition

Extend immutable composition with the canonical job services/backend/repository factory as appropriate.

Likely:

```text
job_service
job_backend
job_executor
```

Do not store a live SQLAlchemy Session in FoundationServices.

Construction must not start threads; lifespan/start method owns worker start.

Avoid mutable globals.

---

# 32. Migration/readiness lifecycle tests

Using isolated temp SQLite:

```text
empty
 -> 20260812_04
 -> 20260812_05
 -> 20260812_04
 -> 20260812_05
```

Verify:

- exactly one Alembic head;
- only `jobs` added by Phase 1H;
- downgrade removes only `jobs`;
- six previous tables remain;
- re-upgrade restores jobs;
- `alembic check` clean;
- prior head `20260812_04` is migration-required/not-ready;
- new head ready under existing readiness semantics;
- liveness remains 200.

Never touch developer default DB.

---

# 33. Job schema tests

Inspect real migrated SQLite and prove:

- exact seven-table ORM allowlist;
- unique job_id;
- required/non-null fields;
- progress check 0..100;
- attempt/max attempt checks;
- allowed status/job type values either DB-constrained or service-constrained;
- timestamps use UTC boundary;
- forbidden credential/traceback/body columns absent;
- artifact/metadata JSON required;
- useful indexes exist.

Actual DB constraint failure tests where applicable.

---

# 34. Repository/state-machine tests

Mandatory tests:

```text
create QUEUED
QUEUED -> RUNNING
RUNNING -> SUCCEEDED
RUNNING -> FAILED
QUEUED -> CANCELLED
RUNNING cancel_requested -> CANCELLED
FAILED -> QUEUED retry
CANCELLED -> QUEUED retry when allowed
SUCCEEDED retry rejected
illegal transitions rejected
double claim prevented
double retry prevented
```

Use real SQLite and competing sessions/threads where concurrency behavior matters.

---

# 35. Local worker execution tests

With trusted test handlers:

### Success handler
- submit;
- runs asynchronously;
- progress persists;
- status reaches SUCCEEDED;
- final progress=100;
- artifact ref persists;
- trace/job context logs correlate.

### Failure handler
- raises exception containing leak markers;
- job becomes FAILED;
- DB contains only safe error;
- runtime log contains safe exception type/frames;
- marker absent from DB/API/log metadata where prohibited;
- retryable policy respected.

### Cancel handler
- handler blocks cooperatively;
- cancel request arrives;
- handler observes cancellation;
- status becomes CANCELLED;
- no forced thread kill.

### Retry
- first attempt fails;
- manual retry queues exactly once;
- second attempt succeeds;
- attempt count correct.

Do not use long sleeps; coordinate with `Event`/`Barrier`.

---

# 36. Recovery tests

Simulate persisted:

```text
RUNNING
```

before worker startup.

On recovery:
- mark FAILED safely;
- set retryable according to policy;
- safe `JOB-WORKER-INTERRUPTED`;
- no raw worker/process details;
- audit/runtime event recorded;
- manual retry can subsequently run if handler registered.

Also test existing QUEUED handling according to the chosen documented startup policy.

No automatic infinite retries.

---

# 37. API tests

With authenticated users:

```text
GET own job                -> 200
GET other user's job       -> same public not-found as absent
GET unknown job            -> safe 404
list jobs                  -> own jobs only
cancel own queued/running  -> accepted/safe
retry own eligible job     -> accepted/safe
cancel/retry without CSRF  -> 403
unauthenticated            -> 401
terminal invalid action    -> safe JOB-* error
```

No ORM object leakage.

No permission list in response.

---

# 38. Audit/log tests

Verify:

- submit/cancel/retry durable audit rows where selected;
- progress ticks do not flood `audit_events`;
- runtime lifecycle logs include job resource IDs;
- same trace/request IDs correlate when job submitted from HTTP context;
- worker-created continuation events carry job trace ID even after original HTTP request is over;
- password/token/CSRF/error marker never leaks.

Because the worker runs outside the HTTP request ContextVar, explicitly persist and re-bind job trace correlation for execution. Do not assume request ContextVars flow forever into future worker tasks.

---

# 39. Worker thread context

The job worker must establish a fresh observability context for each execution.

At minimum bind:

```text
trace_id = persisted job.trace_id
request_id = persisted request_id or generated safe worker request/correlation ID
user_id = owner_user_id when available
resource_type = job
resource_id = job_id
```

Do not inherit stale ContextVars from whichever request thread submitted the work.

Reset context after every job.

Add a two-job concurrency test proving no cross-job user/trace/resource contamination.

---

# 40. Shutdown tests

Prove:

- worker start is idempotent;
- shutdown is safe/idempotent;
- no new jobs accepted after shutdown;
- queued/running state is not falsely marked succeeded because process shuts down;
- test suite does not leak non-daemon threads;
- repeated app/TestClient lifecycle works.

Do not block application shutdown indefinitely on a malicious/non-cooperative handler. Use bounded graceful shutdown policy and document behavior.

Because Python threads cannot be force-killed, a non-cooperative running handler may be marked/recovered on next process start rather than pretending it was cancelled.

---

# 41. Architecture/conformance evolution

Update conformance for exactly seven ORM tables:

```text
audit_events
jobs
permissions
role_permissions
roles
user_sessions
users
```

Verify:

- one DeclarativeBase;
- one Alembic root;
- job ORM only under database/models;
- job DB access only under repository ownership;
- FastAPI routes contain no SQL;
- no Session.query;
- no AsyncSession/async engine/aiosqlite;
- no production create_all;
- no Redis/Celery/RabbitMQ/Kafka;
- no network queue;
- no pickle-based job payloads;
- no dynamic import/exec/eval for handlers;
- no arbitrary callable persisted in DB;
- no JWT/bcrypt/passlib;
- no Streamlit;
- no React/Vue/Angular;
- no runtime CDN;
- no benchmark-specific job type/field names;
- static log-message AST guard remains green.

Do not ban standard-library `ThreadPoolExecutor`.

---

# 42. Dependency policy

Phase 1H should require no new package.

Use:
- standard-library `concurrent.futures`;
- `threading`;
- existing SQLAlchemy/Alembic/FastAPI/Pydantic.

Therefore:

```text
pyproject.toml dependencies unchanged
requirements.lock unchanged
```

Do not regenerate lock.

Do not create a clean dependency-resolution venv.

If a new dependency appears necessary, stop and report before adding it.

---

# 43. Existing security regression

All prior gates remain mandatory:

- Argon2id;
- login timing equalization;
- opaque hash-only sessions;
- session rotation/fixation resistance;
- CSRF;
- lockout;
- password-change invalidation;
- sole RolePermission authorization;
- no Admin-name bypass;
- audit privacy;
- exception safe frames;
- ContextVar isolation;
- multi-sink event identity;
- safe RBAC sync CLI.

Do not weaken these to make jobs easier.

---

# 44. Documentation

Update:

- `database/migrations/README.md`;
- `docs/31_IMPLEMENTATION_PROGRESS.md`;
- `config/README.md` only if job worker has configurable behavior;
- README only if local startup/shutdown usage truly requires it.

Record:

```text
Phase 1H — Persistent Job Service & Local Worker Backend
```

Document:

- job lifecycle;
- seven-table schema;
- local worker architecture;
- cooperative cancellation;
- manual retry;
- safe failure model;
- startup recovery;
- observability/audit behavior;
- generic owner-only job API;
- no domain handlers yet;
- no Redis/Celery;
- migration revision;
- test/quality evidence.

Do not mark:
- job-specific domain operations complete;
- Admin health complete;
- frontend complete;
- Phase 1 complete;
- v0.1.0 complete.

Phase 1I remains next.

---

# 45. Quality gates

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

Migration smoke against isolated DB:

```text
alembic heads
alembic upgrade head
alembic current
alembic check
alembic downgrade 20260812_04
alembic upgrade head
```

No default developer DB.

---

# 46. Phase 1H acceptance gate

PASS only if all are true.

### Contracts
- existing generic JobStatus/JobType preserved;
- no domain contamination;
- clear JobSnapshot/Progress/Error contracts.

### Persistence
- exactly one new `jobs` table;
- seven-table ORM allowlist;
- migration head `20260812_05`;
- safe bounded metadata/artifact refs;
- no arbitrary payload/pickle/secret/traceback storage.

### State machine
- legal transitions enforced;
- illegal transitions rejected;
- retry/cancel race-safe;
- final success progress 100;
- manual retry bounded by attempts.

### Worker
- local in-process bounded executor;
- explicit trusted handler registry;
- no arbitrary code loading;
- cooperative cancellation;
- safe exception capture;
- startup recovery;
- explicit lifecycle/shutdown;
- no cross-job ContextVar leakage.

### Service/API
- persisted before enqueue;
- owner-only generic job GET/list/control;
- CSRF on cancel/retry;
- safe JOB-* errors;
- no ORM leakage;
- no generic arbitrary client submission.

### Observability
- job lifecycle structured logs;
- submit/cancel/retry durable audit;
- worker rebinds persisted job correlation;
- no audit flooding from progress;
- no sensitive leakage.

### Architecture
- sync SQLAlchemy only;
- no Redis/Celery/queue dependency;
- no Phase 1I+ work;
- no frontend/framework/CDN/network drift;
- no benchmark contamination.

### Quality
- full pytest green;
- Ruff green;
- strict mypy green;
- compileall green;
- pip check green;
- diff check green;
- Alembic lifecycle/check green;
- docs accurate.

---

# 47. Mandatory Codex final report

Return every section.

## A. Starting state
- starting SHA
- branch
- initial status

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Job contracts
Report exact JobStatus, JobType, Progress, Error, Snapshot, handler/context contracts.

## E. Job schema
List all columns, constraints, indexes, forbidden-data absence.

## F. Migration
Revision, parent, head/current/check, downgrade/re-upgrade.

## G. Repository
Methods, state-transition concurrency strategy, no-commit ownership.

## H. JobService
Submit/get/list/progress/cancel/retry semantics.

## I. LocalJobBackend / executor
Worker count, queue ownership, handler registration, lifecycle/shutdown.

## J. State machine
Report every allowed transition and tests for illegal transitions.

## K. Cancellation
Queued and running behavior, cooperative acknowledgment, idempotency.

## L. Retry
Eligibility, max attempts, reset behavior, race prevention.

## M. Recovery
Prior RUNNING policy, QUEUED policy, interruption error, retryability.

## N. Job API
Routes, auth, owner isolation, CSRF, public errors.

## O. Observability
Runtime event actions, correlation rebinding, concurrency isolation.

## P. Durable audit
Which job actions persist and why progress does not flood SQLite.

## Q. Privacy/leak evidence
Report markers proving raw exception/password/session/CSRF/token/SQL/path/request-body data absent.

## R. Worker health primitive
Report safe fields and whether readiness was integrated or intentionally deferred to Phase 1I.

## S. Authentication/RBAC/observability regression
Confirm all prior Phase 1E–1G.1 behavior green.

## T. Tests
Exact passed/failed/skipped/warnings.

## U. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, diff check, Alembic lifecycle/check.

## V. Architecture/conformance
Explicitly report:
- ORM allowlist
- ORM/repository ownership
- Session.query
- async DB
- create_all
- Redis/Celery/RabbitMQ/Kafka
- dynamic import/exec/eval/pickle job execution
- JWT/bcrypt/passlib
- Streamlit/framework/CDN
- network queue/logging
- benchmark contamination
- static-message guard

## W. Dependency state
pyproject/lock changes and clean-env status.

## X. Runtime artifacts
DB/WAL/SHM, logs/JSONL, thread/process dumps, venvs/caches.

## Y. Git state
Final status and diff stat.

## Z. Deviations / unresolved issues
If none: `None`

## AA. Gate result

End exactly with one:

`Phase 1H: PASS — ready for independent review before Phase 1I`

or

`Phase 1H: FAIL — Phase 1I blocked`

Do not begin Phase 1I.
