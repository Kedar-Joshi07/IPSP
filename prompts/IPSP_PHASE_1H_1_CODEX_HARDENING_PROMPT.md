# IPSP v1.0 — Phase 1H.1 Codex Worker Shutdown Hardening Prompt
## Bounded Process Shutdown, Safe Persisted Job Decoding & Local-Backend Deployment Constraint

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `0e3be455f7e02490c93db1bc1d1feff81e9e9825`

Phase 1H is structurally strong, but independent review found one blocking local-worker shutdown issue and two small persistence/deployment hardening gaps.

Phase 1I remains blocked until this narrow Phase 1H.1 pass is independently reviewed.

Do not redesign the job state machine, API, audit schema, RBAC, authentication, observability, or database model. Do not add dependencies or migrations. Do not begin Phase 1I.

---

# 1. Read before editing

Read completely:

- `prompts/IPSP_PHASE_1H_CODEX_IMPLEMENTATION_PROMPT.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `backend/ipsp/jobs/contracts.py`
- `backend/ipsp/jobs/local.py`
- `backend/ipsp/jobs/executor.py`
- `backend/ipsp/jobs/service.py`
- `backend/ipsp/repositories/jobs.py`
- `backend/ipsp/observability/context.py`
- `backend/ipsp/main.py`
- `tests/integration/test_job_lifecycle.py`
- `tests/architecture/test_conformance.py`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Start from a clean tracked worktree except for known user-owned prompt files. Do not continue if unrelated tracked changes are already present.

---

# H-001 — Non-cooperative handler can still prevent process termination

The Phase 1H contract explicitly requires:

```text
- no new jobs accepted after shutdown
- queued/running state is not falsely marked succeeded
- test suite does not leak non-daemon threads
- repeated app/TestClient lifecycle works
- application shutdown must not block indefinitely on a malicious/non-cooperative handler
- bounded graceful shutdown
- unresolved running work may be recovered safely on next process start
```

Current `LocalJobBackend` uses:

```python
ThreadPoolExecutor(...)
...
pool.shutdown(wait=False, cancel_futures=True)
```

This makes `shutdown()` return quickly, but a handler already running inside a normal `ThreadPoolExecutor` worker can continue on a **non-daemon** worker thread. If that handler never cooperates or returns, the Python process/interpreter can remain alive waiting for the worker thread.

Therefore `wait=False` alone does not satisfy the Phase 1H process-shutdown guarantee.

## Required behavior

Implement a stdlib-only bounded local worker design such that:

1. `shutdown()` stops job acceptance immediately;
2. queued-but-not-started local work is prevented from executing where practical;
3. a cooperative running handler can finish/cancel normally during a bounded grace period;
4. a permanently non-cooperative handler cannot keep the Python process alive indefinitely;
5. a late-returning handler after shutdown cannot mark the job `SUCCEEDED`;
6. unresolved persisted `RUNNING` work remains recoverable on next worker/process start;
7. the next worker start converts stale `RUNNING` to safe retryable `FAILED` with:
   - `JOB-WORKER-INTERRUPTED`
   - `Job execution was interrupted.`
8. start/shutdown remain idempotent;
9. no new work is accepted after shutdown;
10. no private CPython/concurrent.futures implementation internals are used.

A small explicit bounded daemon-thread worker pool backed by a standard-library queue is an acceptable solution, but it is not mandatory. Choose the smallest maintainable stdlib-only design that satisfies the behavioral contract.

Do **not** solve this with:
- multiprocessing;
- subprocess workers as the production backend;
- force-killing threads;
- Redis/Celery;
- a new dependency;
- private `concurrent.futures` internals.

## Bounded grace period

Use an explicit, documented finite shutdown grace period.

It may be an internal constant rather than a new public Settings field.

Tests must not depend on a long real-time wait. Keep the production default reasonable and make the worker constructor accept a test override if needed.

After the grace period, shutdown must return even if a trusted handler remains permanently blocked.

The job must not be falsely converted to CANCELLED unless the handler actually acknowledges cancellation.

---

# H-001 mandatory subprocess regression

A thread-level unit test is not enough because the defect concerns interpreter/process termination.

Add a deterministic **subprocess-level regression test**.

The parent pytest process should launch a small child Python process that:

1. uses an isolated temporary SQLite DB migrated to `20260812_05`;
2. constructs the local job backend with one trusted test handler;
3. starts one job;
4. the handler signals that it started;
5. the handler then blocks permanently and does not check cancellation;
6. the child calls backend/application shutdown;
7. the child exits normally without releasing the handler.

The parent test must assert the child process exits within a small bounded timeout.

If the child remains alive:
- terminate/kill it in test cleanup;
- fail the test.

Do not let a failing regression hang the test suite.

Also prove, either in the child or a follow-up process/database inspection:

```text
job was not falsely SUCCEEDED
```

Then start a fresh worker/process against the persisted DB and prove stale `RUNNING` recovery produces:

```text
FAILED
JOB-WORKER-INTERRUPTED
retryable = true
```

Use no external process-control dependency.

---

# H-001 additional worker lifecycle regressions

Preserve/add tests proving:

- normal cooperative handler still succeeds;
- cooperative cancellation still reaches `CANCELLED`;
- queued cancellation still reaches `CANCELLED`;
- shutdown is idempotent;
- start is idempotent when already started;
- enqueue after shutdown fails `JOB-WORKER-UNAVAILABLE`;
- repeated `TestClient` / app lifespan usage does not leak active worker infrastructure;
- two simultaneously running jobs retain independent trace/user/resource context;
- late handler completion after shutdown never becomes `SUCCEEDED`.

---

# H-002 — Safely decode persisted job metadata and artifact references

Phase 1H correctly sanitizes/encodes `metadata_json` and validates artifact references before inserting them through the execution context.

However, persistence should have a symmetric safe read boundary.

## Metadata

Add a safe helper such as:

```text
decode_job_metadata(...)
```

Requirements:

- `json.loads` only;
- no `eval`;
- no pickle;
- no object reconstruction;
- return only JSON-safe structures;
- malformed/non-JSON persisted text fails safely to a neutral value such as `{}` or a documented safe exception;
- never return raw Python repr;
- never execute content.

The helper does not need to expose metadata through the public API.

## Artifact references

Strengthen `decode_artifact_references(...)` so persisted strings are revalidated against the same safe relative-reference policy used at write time.

Do not expose through `JobSnapshot` / API any persisted artifact reference that is:

- absolute;
- contains traversal such as `..`;
- contains unsupported characters;
- exceeds the documented bound.

Malformed/unsafe persisted entries should be omitted or fail through a documented safe boundary; they must never become arbitrary local filesystem paths.

Factor the artifact validator so write and read paths use one canonical rule rather than two drifting implementations.

Add corruption/tampering tests using direct DB writes.

---

# H-003 — Document the V1 local backend as single-process

The current local backend has no distributed lease/heartbeat/ownership protocol. Startup recovery intentionally marks persisted `RUNNING` jobs as interrupted.

That is correct for the frozen **local-first single-process** foundation, but it means multiple simultaneously active IPSP application processes sharing the same SQLite jobs database are not a supported worker topology in Phase 1H.

Document this clearly.

Required statement, semantically:

```text
LocalJobBackend is a single-process execution provider.
Do not run multiple active local worker processes against the same control-plane DB.
Multi-process/distributed execution requires a future provider with explicit worker ownership/leases.
```

Do not implement distributed locking, leases, Redis, Celery, worker heartbeats, or a multiprocess coordinator in Phase 1H.1.

Add a small architecture/documentation regression if useful, but do not invent a new runtime network mechanism.

---

# 2. Scope lock

Do NOT change:

- `jobs` schema;
- migration `20260812_05`;
- seven-table ORM allowlist;
- JobStatus;
- JobType;
- allowed lifecycle transitions;
- owner-only API policy;
- API route set;
- CSRF/auth behavior;
- RBAC authority;
- error taxonomy except if a purely internal safe worker shutdown code is absolutely necessary;
- audit table/schema;
- existing job audit action names;
- JSONL observability contract;
- `pyproject.toml`;
- `requirements.lock`;
- frontend;
- readiness/Admin health;
- Phase 1I.

No migration is expected.

No dependency is expected.

---

# 3. Preserve existing Phase 1H behavior

All of these must stay green:

```text
QUEUED -> RUNNING
QUEUED -> CANCELLED
RUNNING -> SUCCEEDED
RUNNING -> FAILED
RUNNING -> CANCELLED
FAILED/CANCELLED -> QUEUED retry
SUCCEEDED retry denied

single-winner claim
single-winner retry
manual bounded retry
safe enqueue failure
safe handler failure
owner-only GET/list/cancel/retry
cross-owner indistinguishable from absent
CSRF on cancel/retry
job.submit/job.cancel/job.retry audit
interrupted recovery audit
progress runtime-only
safe stack diagnostics
worker ContextVar rebinding/isolation
```

Do not weaken a previous regression to make shutdown tests pass.

---

# 4. Architecture/conformance

Preserve:

```text
audit_events
jobs
permissions
role_permissions
roles
user_sessions
users
```

as the exact ORM allowlist.

Keep:

- one DeclarativeBase;
- one Alembic root;
- job ORM only under `database/models`;
- SQL access under repository ownership;
- synchronous SQLAlchemy;
- no `Session.query`;
- no AsyncSession/async engine/aiosqlite;
- no production `create_all`;
- no Redis/Celery/RabbitMQ/Kafka;
- no network queue;
- no dynamic import/exec/eval;
- no pickle job execution;
- no arbitrary callable persisted in DB;
- no JWT/bcrypt/passlib;
- no Streamlit/React/Vue/Angular;
- no runtime CDN;
- no benchmark contamination;
- static literal logger-message AST guard.

If replacing `ThreadPoolExecutor`, update architecture tests only as required by the new canonical local-worker implementation. Do not loosen other bans.

---

# 5. Documentation

Update:

- `docs/31_IMPLEMENTATION_PROGRESS.md`
- README/config documentation only if necessary to make the single-process local-backend constraint discoverable

Add:

```text
Phase 1H.1 — Local Worker Shutdown & Persistence Hardening
```

Record:

- bounded process shutdown;
- non-cooperative-handler subprocess regression;
- no false terminal success after shutdown;
- restart recovery behavior;
- safe metadata decoding;
- artifact-reference read validation;
- LocalJobBackend single-process deployment constraint;
- no schema/migration/dependency changes;
- exact test/quality evidence.

Do not mark Phase 1 complete.

Do not begin Phase 1I.

---

# 6. Mandatory verification

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
alembic check
```

Expected:

```text
Alembic head = 20260812_05
ORM tables = exactly 7
pyproject.toml unchanged
requirements.lock unchanged
migration 20260812_05 unchanged
```

Run the subprocess shutdown regression as part of ordinary pytest.

Do not claim PASS unless it actually ran.

---

# 7. Git discipline

Before and after:

```text
git status --short
git rev-parse HEAD
git diff --stat
git diff --check
```

Start from a clean tracked worktree.

Do not commit:
- test DB/WAL/SHM files;
- logs/JSONL;
- subprocess marker files outside temp dirs;
- process/thread dumps;
- venvs;
- caches;
- credentials/tokens;
- generated archives.

Preserve user-owned prompt files.

---

# 8. Mandatory Codex final report

## A. Starting state
- SHA
- branch
- initial git status
- confirm no unrelated tracked changes before implementation

## B. Files created
Every file.

## C. Files modified
Every file.

## D. H-001 worker shutdown architecture
Report:
- worker implementation type;
- daemon/non-daemon behavior;
- worker count bound;
- shutdown grace policy;
- what happens to queued work;
- what happens to a non-cooperative running handler;
- why process exit is bounded.

## E. Subprocess shutdown proof
Report:
- child setup;
- permanent blocking handler behavior;
- shutdown timing/timeout;
- child exit result;
- false-success check;
- follow-up recovery result.

## F. Existing worker lifecycle regression
Report:
- normal success;
- cooperative cancellation;
- queued cancellation;
- retry;
- start/shutdown idempotency;
- enqueue-after-shutdown;
- late-completion suppression;
- context isolation.

## G. H-002 safe persistence decoding
Report:
- metadata decoding;
- malformed JSON behavior;
- artifact validation on read;
- traversal/absolute-path rejection;
- canonical validator ownership.

## H. H-003 deployment constraint
State exactly how the single-process local-worker limitation is documented and confirm no distributed-lock implementation was added.

## I. Schema/migration/dependencies
Confirm:
- migration head `20260812_05`;
- migration unchanged;
- seven-table allowlist unchanged;
- pyproject unchanged;
- lock unchanged;
- no new dependency.

## J. Authentication/RBAC/observability/job regression
Confirm all Phase 1E through Phase 1H behavior remains green.

## K. Tests
Exact:
- passed
- failed
- skipped
- warnings
- subprocess worker-shutdown test result

## L. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, diff check, Alembic heads/check.

## M. Runtime artifacts
DB/WAL/SHM, logs, subprocess leftovers, thread/process dumps, venvs/caches.

## N. Phase boundary
Confirm no Phase 1I or later-domain implementation.

## O. Git state
Final status and diff stat.

## P. Deviations / unresolved issues
If none:
`None`

## Q. Gate result

End exactly with:

`Phase 1H.1: PASS — Phase 1I ready for independent review`

or

`Phase 1H.1: FAIL — Phase 1I blocked`

Do not begin Phase 1I.
