# IPSP v1.0 — Phase 1H.2 Codex Worker Authority Hardening Prompt
## Atomic Shutdown/Execution Authority + Abandoned-Generation Restart Safety

**Repository:** `Kedar-Joshi07/IPSP`
**Required starting point:** `7718605ff2828b07f1d7d5c0d8c1ad5515576580`

Phase 1H.1 successfully fixed the original process-termination defect: the local worker now uses bounded daemon threads, the subprocess regression proves a permanently blocked handler cannot keep the process alive, persisted RUNNING work survives shutdown, and a fresh process recovers it safely.

Independent review found one remaining concurrency defect in the new generation-scoped execution-authority mechanism. Phase 1I remains blocked until this narrow Phase 1H.2 hardening pass is independently reviewed.

Do not redesign jobs. Do not add dependencies or migrations. Do not begin Phase 1I.

---

# 1. Read before editing

Read completely:

- `prompts/IPSP_PHASE_1H_CODEX_IMPLEMENTATION_PROMPT.md`
- `prompts/IPSP_PHASE_1H_1_CODEX_HARDENING_PROMPT.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `backend/ipsp/jobs/local.py`
- `backend/ipsp/jobs/executor.py`
- `backend/ipsp/repositories/jobs.py`
- `backend/ipsp/jobs/service.py`
- `backend/ipsp/database/session.py`
- `tests/integration/test_job_lifecycle.py`
- `tests/architecture/test_conformance.py`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Start from a clean tracked worktree except known user-owned prompt files.

---

# H-001 — Generation authority checks are snapshots, not atomic persistence authority

Current Phase 1H.1 introduces:

```python
class JobExecutionLifecycle:
    ...
    @contextmanager
    def starting_allowed(self):
        yield not self._stopping.is_set()

    @contextmanager
    def completion_allowed(self):
        yield not self._abandoned.is_set()
```

and execution code performs persistence after receiving the yielded Boolean.

This creates a check/use race.

Example terminal race:

```text
worker:
    completion_allowed() -> True
    [scheduler pause]

shutdown:
    grace expires
    lifecycle.abandon()
    shutdown returns

worker resumes:
    mark_succeeded(...)
```

The Boolean was frozen before `abandon()`, so the job can still be persisted as `SUCCEEDED` after the generation has lost completion authority.

The same class of race exists for:

```text
starting_allowed() -> mark_running()
_raise_if_abandoned() -> update_progress()
_raise_if_abandoned() -> add_artifact_reference()
cancellation terminal write
failure terminal write
```

Phase 1H.1 documentation currently claims:

```text
A handler returning after grace cannot persist progress or a false terminal result.
```

That guarantee must be made true under deterministic interleaving, not merely in the common execution order.

---

# 2. Required authority semantics

Create one canonical synchronization mechanism in `JobExecutionLifecycle` that makes generation authority and worker-owned persistence mutually consistent.

Required guarantees:

## Starting authority

Once shutdown has successfully revoked "start new work" authority:

- a worker that had not already acquired start authority must not move a QUEUED job to RUNNING;
- queued persisted jobs remain QUEUED;
- workers that legitimately acquired start authority before shutdown may finish the short claim transaction.

## Completion/persistence authority

Once `abandon()` has successfully revoked persistence/completion authority:

- no old-generation worker may newly persist:
  - progress;
  - artifact references;
  - SUCCEEDED;
  - FAILED;
  - CANCELLED;
- no old-generation terminal runtime event may falsely describe a suppressed state transition as persisted;
- the stale row remains recoverable on the next process/worker startup.

## Atomicity

The authority decision must not be a Boolean snapshot that is later used without synchronization.

The preferred shape is a lifecycle-owned lock/lease/context that remains authoritative for the short persistence operation, for example conceptually:

```python
with lifecycle.start_authority() as allowed:
    if not allowed:
        return
    # short QUEUED -> RUNNING transaction occurs while authority is held
```

and:

```python
with lifecycle.persistence_authority() as allowed:
    if not allowed:
        raise JobExecutionAbandoned()
    # one short worker-owned DB persistence action occurs while authority is held
```

Exact API/naming may differ.

`stop_starting()` and `abandon()` must synchronize against those leases rather than merely setting an Event that can race after a prior check.

Do not hold lifecycle authority across arbitrary handler execution. Hold it only across short infrastructure-owned persistence/claim operations.

---

# 3. Preserve bounded shutdown

Do not reintroduce the original Phase 1H defect.

The subprocess test with a permanently blocked handler must continue to prove:

```text
shutdown is bounded
child process exits
job is not falsely SUCCEEDED
fresh process recovers JOB-WORKER-INTERRUPTED
```

A lifecycle synchronization lock must **not** be held while arbitrary handler code runs.

If shutdown waits for an already-started short DB state write to complete, that is acceptable, but the worker design must not wait indefinitely on handler execution.

Keep daemon-thread workers and bounded shutdown grace.

---

# 4. Abandoned-generation restart safety

A second safety issue follows from abandonment.

After shutdown grace expires, current code clears generation state and permits `start()` again even if an old abandoned daemon handler is still alive.

Do not allow two generations of the **same LocalJobBackend** to overlap while abandoned prior-generation worker threads remain alive.

Required policy:

```text
cooperative/finished old generation
    -> restart allowed

abandoned old generation with live daemon thread(s)
    -> same backend start fails safely with JOB-WORKER-UNAVAILABLE

fresh process / fresh backend after actual process restart
    -> startup recovery works as designed
```

Once all abandoned old-generation threads have naturally exited, a same-process restart may become allowed if implementation can verify that safely.

Do not force-kill threads.

Do not recover a RUNNING job in the same process while the old generation that owns its handler can still be executing.

This protects future handlers from duplicate external side effects even though old-generation IPSP persistence is suppressed.

---

# 5. Deterministic race tests

Do not rely on probabilistic timing loops.

Add deterministic interleaving tests using Events/Barriers/test hooks around lifecycle authority.

At minimum prove:

### A. Completion vs abandon

Force this order:

```text
handler has returned / terminal persistence is about to request authority
shutdown reaches abandonment
old-generation terminal path continues
```

Expected:

```text
job remains RUNNING
not SUCCEEDED
not FAILED
not CANCELLED
```

until recovery.

### B. Progress vs abandon

Force a late progress call after abandonment.

Expected:
- `JobExecutionAbandoned` internal control flow or equivalent;
- persisted progress unchanged.

### C. Artifact vs abandon

Force a late artifact write after abandonment.

Expected:
- artifact not persisted/exposed.

### D. Start claim vs stop_starting

Interleave a queued worker and shutdown so shutdown revokes start authority before the worker obtains its persistence lease.

Expected:
- job remains QUEUED, not RUNNING.

### E. Already-authorized short operation

Prove an infrastructure persistence operation that acquired authority before revocation can complete cleanly without corrupting state.

This prevents an overcorrection where normal short DB actions are spuriously interrupted.

### F. Restart with abandoned live worker

Keep an abandoned handler alive, then call the same backend's `start()`.

Expected:

```text
JOB-WORKER-UNAVAILABLE
```

Release old handler, wait for its daemon thread to exit, and verify restart behavior according to the documented implementation.

---

# 6. Phase 1H.1 regressions must remain green

Preserve all existing 1H.1 evidence:

- permanent-block subprocess exits within timeout;
- fresh-process interrupted recovery;
- daemon worker proof;
- graceful completion during shutdown grace;
- no false success from an ordinary late completion;
- repeated TestClient lifespans when workers stop normally;
- cooperative cancellation;
- queued cancellation;
- retry;
- owner-only API;
- audit;
- ContextVar isolation;
- safe metadata decoding;
- artifact validation;
- single-process deployment documentation.

Do not weaken/remove the subprocess test.

---

# 7. Scope lock

Do NOT change:

- jobs ORM schema;
- migration `20260812_05`;
- seven-table ORM allowlist;
- JobStatus;
- JobType;
- public job API routes;
- owner-only API policy;
- CSRF/auth/RBAC behavior;
- retry attempt semantics;
- audit schema;
- established job audit action names;
- observability envelope;
- readiness;
- frontend;
- `pyproject.toml`;
- `requirements.lock`;
- Phase 1I.

No dependency or migration is expected.

---

# 8. Documentation

Update `docs/31_IMPLEMENTATION_PROGRESS.md` with:

```text
Phase 1H.2 — Atomic worker-generation authority hardening
```

Record:

- start/persistence authority is now synchronized rather than Boolean-snapshot based;
- abandonment prevents all subsequent old-generation progress/artifact/terminal writes;
- shutdown remains bounded because arbitrary handlers never hold authority locks;
- same-backend restart is rejected while abandoned previous-generation threads remain alive;
- deterministic race tests;
- subprocess termination/recovery remains green;
- no schema/migration/dependency changes.

Do not mark Phase 1 complete.

README changes are not required unless restart policy needs a small clarification.

---

# 9. Mandatory verification

Run:

```text
python -m compileall -q backend tests
pytest
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
alembic heads
alembic check
```

Confirm:

```text
Alembic head = 20260812_05
ORM allowlist = exactly seven tables
migration 20260812_05 unchanged
pyproject.toml unchanged
requirements.lock unchanged
no Phase 1I code
```

The subprocess non-cooperative shutdown test must run as part of ordinary pytest.

---

# 10. Mandatory Codex final report

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Atomic lifecycle authority
Explain the synchronization primitive and exactly when authority is held.

## E. Start-authority race
Explain how QUEUED -> RUNNING is protected against shutdown interleaving.

## F. Persistence-authority race
Explain protection for progress, artifacts, success, failure and cancellation.

## G. Bounded shutdown
Confirm handler code never holds authority synchronization and subprocess termination remains bounded.

## H. Abandoned-generation restart
Explain same-backend restart policy while old threads are alive and after they exit.

## I. Deterministic race evidence
Report each forced interleaving test and expected persisted result.

## J. Phase 1H.1 regression
Report subprocess shutdown/recovery, daemon workers, safe decoding/artifacts, lifecycle/API/audit/context regressions.

## K. Schema/dependency state
Confirm migration/table/pyproject/lock unchanged.

## L. Tests
Exact passed/failed/skipped/warnings.

## M. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, diff check, Alembic heads/check.

## N. Runtime artifacts
Confirm no DB/WAL/SHM/log/subprocess leftovers/dumps/venv artifacts.

## O. Phase boundary
Confirm no Phase 1I work.

## P. Git state
Final status + diff stat.

## Q. Deviations / unresolved issues
If none: `None`

## R. Gate result

End exactly with:

`Phase 1H.2: PASS — Phase 1I ready for independent review`

or

`Phase 1H.2: FAIL — Phase 1I blocked`

Do not begin Phase 1I.
