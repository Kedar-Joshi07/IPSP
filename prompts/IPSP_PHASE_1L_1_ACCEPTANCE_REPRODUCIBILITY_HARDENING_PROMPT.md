# IPSP v1.0 — Phase 1L.1 Codex Acceptance-Reproducibility Hardening Prompt
## Permanent-Blocked-Worker Regression Determinism + Final v0.1.0 Re-Audit

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `d8c4db477f7d213516589658435be142a9dc9e89`

Current independent state:
- Phase 1A through Phase 1K: accepted
- Phase 1L audit: correctly FAIL
- Acceptance blocker: `PHASE1L-B001`
- v0.1.0: NOT accepted
- v0.2: BLOCKED
- No production defect has been confirmed
- No production source was changed in Phase 1L

This task is **Phase 1L.1 only**.

The purpose is to determine whether `PHASE1L-B001` is a test-harness timing problem or a real process-lifecycle defect, harden the regression so it measures the intended invariant directly, and then repeat the final acceptance audit.

Do not begin v0.2.
Do not create a Git tag or GitHub release.

---

# 1. Starting evidence

The Phase 1L audit observed:

```text
Full suite:
216 collected
215 passed
1 failed
0 skipped

Failure:
tests/integration/test_job_lifecycle.py::
test_noncooperative_daemon_worker_cannot_hold_child_process_and_recovers
```

The failed outer assertion was:

```text
blocked.communicate(timeout=10)
```

The same complete job-lifecycle module subsequently passed:

```text
18 passed
```

The child independently measures:

```text
backend.shutdown() elapsed < 0.5 seconds
```

Therefore the current evidence establishes an acceptance reproducibility blocker, not yet a confirmed production defect.

The outer `communicate(timeout=10)` currently measures Python startup, imports, provider construction, SQLite access, worker scheduling, handler startup, backend shutdown, DB disposal, and interpreter exit in one aggregate deadline.

Phase 1L.1 must separate setup latency from the actual daemon-worker process-exit invariant instead of merely increasing the timeout.

---

# 2. Read before editing

Read completely:
- `docs/PHASE_1_ACCEPTANCE_REPORT.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `tests/integration/test_job_lifecycle.py`
- `backend/ipsp/jobs/local.py`
- `backend/ipsp/jobs/executor.py`
- `backend/ipsp/jobs/service.py`
- `backend/ipsp/config/providers.py`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `prompts/IPSP_PHASE_1L_FINAL_ACCEPTANCE_AUDIT_PROMPT.md`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Expected SHA:

```text
d8c4db477f7d213516589658435be142a9dc9e89
```

---

# 3. Production-code stop rule

Expected production changes: **NONE**.

Do not change:
- `backend/ipsp/**`
- `frontend/**`
- `database/migrations/**`
- `pyproject.toml`
- `requirements.lock`

unless the new deterministic protocol proves a genuine production defect.

If the child reaches a clearly signaled "normal cleanup complete" point and then the process still cannot terminate within the dedicated post-marker exit bound:
- do not patch production code inside Phase 1L.1;
- record the evidence;
- mark Phase 1L.1 FAIL;
- leave v0.1.0 unaccepted;
- leave v0.2 blocked.

---

# 4. H-001 — Test the actual invariant directly

The regression must independently prove BOTH:

## A. Bounded backend shutdown

The child must continue to measure:

```text
shutdown_started = time.monotonic()
backend.shutdown()
elapsed = time.monotonic() - shutdown_started
```

and the parent must continue to assert:

```text
elapsed < 0.5
```

Do not relax this bound merely to make the test green.

## B. Permanently blocked daemon work cannot hold process exit

Do not use one aggregate `communicate(timeout=N)` as the sole proof.

Introduce an explicit completion protocol:

1. Start the child with stdout/stderr pipes.
2. Child starts the permanently blocked handler.
3. Child calls `backend.shutdown()`.
4. Child reads the persisted job snapshot.
5. Child disposes normal database resources.
6. Child emits one final JSON line with `print(..., flush=True)` containing at least:
   - `job_id`
   - `status`
   - `elapsed`
   - `"stage": "normal_cleanup_complete"`
7. After that marker, the child script has no intentional normal work left. The blocked daemon worker is the remaining relevant lifecycle condition.
8. Parent gives setup/import/protocol completion a reasonable bounded allowance.
9. Only after receiving the marker, parent starts a dedicated process-exit deadline.
10. Require process exit within a small fixed bound, recommended 2 seconds.
11. If it does not exit, kill/reap it and fail specifically:
   `Blocked daemon worker prevented process exit after normal cleanup`.
12. Always reap stdout/stderr and the child process.

This separates environment/setup latency from daemon-worker process-exit correctness.

Do NOT solve this by changing `communicate(timeout=10)` to a larger number and nothing else.

---

# 5. Suggested parent-side protocol

A daemon pipe-reader thread plus `Queue`/`Event` is acceptable and cross-platform.

Conceptually:

```text
Popen child
    ↓
daemon reader waits for one stdout JSON line
    ↓
parent allows bounded setup/protocol time
    ↓
parse and validate stage
    ↓
assert child-reported shutdown elapsed < 0.5
    ↓
start exit timer NOW
    ↓
child.wait(timeout=2)
    ↓
assert clean return code
```

Do not use an unbounded blocking `readline()` in the pytest thread.

Do not add a third-party dependency.

A temporary sentinel/result file is also acceptable if the same two-stage timing semantics are preserved.

---

# 6. Child-process hygiene

Strengthen cleanup so a failed regression cannot leave orphan processes.

For each subprocess in this test:
- if still alive, kill it;
- wait/reap it;
- read remaining stdout/stderr;
- close pipes.

Use `finally`-safe cleanup.

Do not introduce Unix-only process-group APIs.

---

# 7. Recovery child

The recovery child was not the observed blocker. Do not redesign it unnecessarily.

Its functional assertion must remain:

```text
status = FAILED
error_code = JOB-WORKER-INTERRUPTED
retryable = true
```

A shared safe subprocess helper is allowed if it improves ownership/reaping without weakening the test.

---

# 8. No product-timeout inflation

Keep the distinction explicit:

```text
Product invariant:
backend.shutdown() < 0.5 seconds
process exits shortly after normal cleanup despite blocked daemon handler

Harness allowance:
child startup/import/setup may take longer under machine load
```

A larger setup allowance is acceptable.

The post-marker process-exit deadline must remain small and explicit.

---

# 9. Stability verification — planned, not retry-until-green

All planned runs must pass.

## Gate A — exact blocker test

Run the exact test in three separate pytest process invocations:

```text
pytest tests/integration/test_job_lifecycle.py::test_noncooperative_daemon_worker_cannot_hold_child_process_and_recovers
```

Required: **3/3 PASS**.

If any invocation fails, Phase 1L.1 fails.

## Gate B — complete job lifecycle

Run:

```text
pytest tests/integration/test_job_lifecycle.py
```

Required: all pass.

## Gate C — full-suite reproducibility

Run the full suite twice as two predeclared clean invocations:

```text
pytest
pytest
```

Required for both:
- 0 failed
- 0 skipped
- 0 warnings

If either run fails, Phase 1L.1 fails.

This is not "rerun until green"; both runs are mandatory planned evidence.

## Gate D — Phase 1K focused proof

Run:

```text
pytest tests/integration/test_phase1_foundation_e2e.py tests/security/test_phase1_security_boundaries.py
```

Required: all pass.

---

# 10. Browser QA ordering and cleanup

The Phase 1L browser QA temporarily left an orphaned Uvicorn child retaining QA files.

For Phase 1L.1:
1. Run Python acceptance/test gates before browser QA.
2. Browser QA must use an isolated DB/log directory.
3. Explicitly terminate/reap the QA Uvicorn process after checks.
4. Verify the QA port has no listener afterward.
5. Verify the QA DB/log directory can be removed.
6. Avoid oversized full-DOM snapshots; inspect only needed DOM fragments/state.
7. Browser-extension message-channel noise is tooling noise, not an app failure.
8. Application-origin console exceptions/errors are failures.

Do not let external browser tooling contaminate pytest process state.

---

# 11. Final browser acceptance

If the same browser facility is available, recheck:

## Admin
- Login
- Overview
- Jobs
- Profile
- System Health
- System / Dark / Light
- Logout

## Permission denial
- ordinary user
- `#/admin/system`
- dedicated permission state

## Required password
- forced password-change screen
- normal navigation blocked
- Sign out works

## Responsive
- desktop
- approximately 390px mobile

Confirm:
- no horizontal overflow;
- all runtime assets same-origin;
- only theme localStorage;
- session cookie unavailable to JS;
- no stale route overwrite;
- no application-origin console error.

---

# 12. Acceptance-report classification correction

Independent review found one classification that should be corrected.

Criterion #14 from `docs/30_ACCEPTANCE_CRITERIA.md`:

```text
Unsupported capabilities are visibly disabled with reasons.
```

was classified PASS based on foundation roadmap UI.

That criterion belongs to actual capability discovery. The capability-discovery engine is not implemented in v0.1.0.

Classify criterion #14:

```text
DEFERRED_BY_ROADMAP
```

Do not use static roadmap cards as evidence that capability refusal/disablement is implemented.

If the jobs blocker is resolved, criterion #31 becomes PASS.

Expected successful classification totals:

```text
PASS: 15
DEFERRED_BY_ROADMAP: 22
NOT_APPLICABLE: 0
BLOCKED: 0
TOTAL: 37
```

Recalculate from the actual matrix.

---

# 13. Acceptance report update

Update in place:

```text
docs/PHASE_1_ACCEPTANCE_REPORT.md
```

Do not create a competing report.

Preserve the historical fact that original Phase 1L failed, but make the current decision reflect the Phase 1L.1 re-audit.

If PASS:
- explain `PHASE1L-B001` was traced to the aggregate test-harness deadline rather than a confirmed production shutdown failure;
- document the two-stage subprocess protocol;
- record 3/3 targeted passes;
- record complete job-lifecycle pass;
- record both full-suite passes;
- record Phase 1K focused pass;
- set Jobs and Integration/Security to PASS;
- set criterion #31 to PASS;
- set criterion #14 to DEFERRED_BY_ROADMAP;
- set BLOCKED total to 0;
- state no production defect was found;
- recommend v0.1.0 acceptance pending independent final review.

Do not erase the original failed evidence.

---

# 14. README behavior

Only if every Phase 1L.1 gate passes:

Update README implementation status to equivalent wording:

```text
Implementation status: Phase 1 / v0.1.0 foundation accepted pending independent final review
```

Also state:

```text
Next planned milestone: v0.2.0 ingestion/storage/provenance
```

but explicitly:

```text
not started; blocked until independent Phase 1L.1 acceptance
```

Preserve all statements that ingestion, profiling, semantics, modelling, simulation, reports, and LLM execution remain unimplemented.

If Phase 1L.1 fails, do not mark Phase 1 complete.

---

# 15. Implementation progress

Update:

```text
docs/31_IMPLEMENTATION_PROGRESS.md
```

Add:

```text
Phase 1L.1 — Acceptance Reproducibility Hardening
```

Record:
- original blocker;
- test-protocol diagnosis;
- exact harness change;
- production code unchanged;
- 3/3 blocker stability result;
- complete job lifecycle result;
- both planned full-suite results;
- Phase 1K focused rerun;
- browser/repository hygiene;
- final decision.

If PASS, Phase 1 row may say:

```text
PHASE 1 COMPLETE — v0.1.0 foundation accepted pending independent final review
```

Do not start v0.2.

---

# 16. Dependency clean-install evidence

Phase 1L skipped the disposable clean install after the blocker.

Attempt it in Phase 1L.1 if environment access permits, using a disposable temporary environment outside persistent project state.

Verify:
- install from `requirements.lock`;
- install project with `--no-deps`;
- import `ipsp`;
- construct Settings/app safely;
- `pip check`.

Remove the environment afterward.

If package-index/network availability prevents this:
- report the exact environmental limitation;
- do not claim it passed;
- still require lock consistency and current-environment `pip check`.

A broken/inconsistent lock is a blocker.

Do not regenerate dependencies merely to make the audit pass.

---

# 17. Quality gates

Run:

```text
python -m compileall -q backend tests
ruff check .
ruff format --check .
mypy backend/ipsp
pip check
git diff --check
```

Run isolated Alembic:

```text
alembic heads
alembic current
alembic check
```

Expected:

```text
head = 20260812_05
ORM application tables = 7
```

No migration/schema/dependency changes.

---

# 18. Repository residue

Before final report confirm no:
- orphan Python/Uvicorn child;
- QA port listener;
- test DB;
- WAL/SHM;
- runtime QA logs;
- browser profile;
- oversized DOM snapshot;
- temp virtualenv;
- node_modules;
- dist;
- credentials/cookies;
- secret marker files.

---

# 19. Expected PASS diff

Expected tracked changes on PASS:

```text
tests/integration/test_job_lifecycle.py
docs/PHASE_1_ACCEPTANCE_REPORT.md
docs/31_IMPLEMENTATION_PROGRESS.md
README.md
prompts/IPSP_PHASE_1L_1_ACCEPTANCE_REPRODUCIBILITY_HARDENING_PROMPT.md
```

Production application files should not change.

No migration/dependency changes.

---

# 20. Phase boundary

Do NOT:
- begin ingestion;
- create dataset/ACL tables;
- add Parquet;
- add upload endpoints;
- add LLM/model/simulation code;
- create a tag;
- create a release;
- bump beyond 0.1.0.

PASS means only:

```text
v0.1.0 foundation is ready for independent final acceptance
```

Independent review decides whether v0.2 is authorized.

---

# 21. Mandatory Codex final report

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every retained file.

## C. Files modified
Every file.

## D. PHASE1L-B001 diagnosis
Explain why aggregate `communicate(timeout=10)` was not a precise process-exit measurement.

## E. New subprocess protocol
Report:
- setup allowance;
- completion marker;
- preserved shutdown `< 0.5`;
- dedicated post-marker exit bound;
- cleanup/reaping.

## F. Production defect conclusion
Expected on PASS:
`No production defect confirmed.`

## G. Targeted stability
Report all three planned exact-test invocations individually.

## H. Job lifecycle
Exact result/duration.

## I. Full-suite reproducibility
Report Run 1 and Run 2 separately:
- passed
- failed
- skipped
- warnings
- duration

Both must pass.

## J. Phase 1K focused rerun
Exact result.

## K. Browser acceptance
Report journeys, responsive state, app-origin console state, asset origin, cleanup.

## L. V1 classification correction
Report:
- criterion #14;
- criterion #31;
- final PASS/DEFERRED/NA/BLOCKED totals.

## M. Acceptance matrix
Report all Phase 1 categories and confirm zero BLOCKED categories on PASS.

## N. Security/privacy
Confirm prior auth/session/CSRF/RBAC/redaction/outbound guards remain green.

## O. Database/migration
Head, seven tables, FK, sync DB, no drift.

## P. Dependency reproducibility
Current `pip check`, lock state, clean-install result or exact environmental limitation.

## Q. Quality gates
Compileall, Ruff, format, mypy, pip, diff, Alembic.

## R. Production source changes
Expected:
`None`

## S. Schema/dependency changes
Expected:
`None`

## T. Acceptance report
Confirm updated:
`docs/PHASE_1_ACCEPTANCE_REPORT.md`

## U. README status
Report exact implementation-status wording.

## V. Progress status
Report exact Phase 1 row/status wording.

## W. Repository/runtime residue
Report orphan-process/port/DB/log/browser/temp-environment cleanup.

## X. Phase boundary
Confirm v0.2 not started and no tag/release created.

## Y. Deviations / unresolved issues
If none:
`None`

## Z. Gate result

End exactly with one:

`Phase 1L.1: PASS — v0.1.0 foundation ready for independent final acceptance; v0.2 remains blocked`

or

`Phase 1L.1: FAIL — v0.1.0 foundation not accepted; v0.2 blocked`

Do not begin v0.2.
