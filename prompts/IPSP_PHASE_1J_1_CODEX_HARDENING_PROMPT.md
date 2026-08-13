# IPSP v1.0 — Phase 1J.1 Codex Frontend Lifecycle Hardening Prompt
## Route Concurrency, Theme-System Semantics, Jobs Action-State Correctness & Readiness UX

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `1e5c35233d5782b65ab0482de7ef552447b80361`

Phase 1J establishes the correct production UI architecture and visual system, but independent review found a small set of frontend runtime correctness gaps that must be hardened before Phase 1K.

Phase 1K remains blocked until this narrow Phase 1J.1 pass is independently reviewed.

Do not redesign the UI. Do not add a framework, dependency, migration, backend domain feature, or new permission. Do not begin Phase 1K.

---

# 1. Read before editing

Read completely:

- `prompts/IPSP_PHASE_1J_CODEX_IMPLEMENTATION_PROMPT.md`
- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `frontend/index.html`
- `frontend/js/app.js`
- `frontend/js/router.js`
- `frontend/js/state.js`
- `frontend/js/api.js`
- `frontend/js/theme.js`
- `frontend/js/components.js`
- `frontend/js/dom.js`
- `frontend/js/views/login.js`
- `frontend/js/views/overview.js`
- `frontend/js/views/jobs.js`
- `frontend/js/views/profile.js`
- `frontend/js/views/system-health.js`
- `tests/integration/test_frontend.py`
- `tests/integration/test_app.py`
- `tests/architecture/test_conformance.py`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Start from a clean tracked worktree except known user-owned prompt files.

---

# H-001 — Hash-route lifecycle has an async stale-render race

The Phase 1J contract requires route changes to clean up page-specific work.

Current router/app flow is approximately:

```text
hashchange
  -> dispatch()
  -> await renderRoute(route)
  -> save returned cleanup
```

but `renderRoute()` currently does not return the cleanup returned by the individual views.

More importantly, even if that return is wired, `startRouter()` can receive a second hashchange while the previous asynchronous route is still awaiting API data.

That creates a race such as:

```text
#/jobs begins loading
        ↓
user navigates to #/profile
        ↓
profile renders
        ↓
older jobs request completes
        ↓
old jobs view clears/replaces shared <main>
```

The URL/navigation state can therefore say Profile while stale Jobs/Overview/System Health content wins the DOM.

This must be impossible.

## Required behavior

Implement one canonical route-generation / cancellation mechanism.

Acceptable designs include:

- `AbortController`/`AbortSignal`;
- monotonically increasing route generation/token;
- another explicit equivalent.

Required guarantees:

1. each route render has a unique active lifecycle;
2. navigating again immediately invalidates the previous lifecycle;
3. previously registered cleanup runs exactly once;
4. an async result from an invalidated route cannot mutate the shared main container;
5. an invalidated route cannot install itself as the new cleanup after a later route won;
6. open Jobs confirmation dialogs close on route exit;
7. pending login readiness callbacks cannot mutate detached/current-route UI;
8. page-specific future timers/pollers have one obvious cleanup boundary;
9. route focus/title/navigation state reflects only the winning route;
10. no global application state is moved onto `window`.

Do not solve this with arbitrary sleeps.

Do not serialize navigation by blocking the user until a prior request finishes.

## Recommended shape

A router-owned `AbortController` is appropriate, e.g. conceptually:

```text
dispatch new route
    -> abort previous route signal
    -> run previous cleanup
    -> create new signal
    -> call onRoute(route, signal)
    -> if route was superseded, discard/cleanup returned work
```

Views that await data must check route activity before DOM mutation.

Passing the signal through the same-origin API client is acceptable and preferable if done cleanly, but aborted fetches must be treated as silent route disposal rather than user-facing failures.

Exact API may differ.

---

# H-001 mandatory deterministic regression

Add deterministic browser/runtime coverage where the existing test environment supports it.

Prove this order:

```text
Jobs/Overview async request starts
Profile route renders
old request resolves afterward
```

Expected:

```text
current route remains Profile
Profile DOM remains present
old route does not replace <main>
no stale error/flash is rendered
```

Also prove:

```text
open Jobs cancellation dialog
navigate away
dialog is removed/closed
```

If the repository's automated Python environment cannot execute ES modules directly, preserve source-level architecture assertions and perform the existing browser execution QA deterministically. Do not add Node/npm or a JS test framework solely for this patch.

---

# H-002 — View cleanup return values are currently discarded

Several views already return cleanup functions:

- Login;
- Jobs;
- Profile;
- required-password view.

Wire these into the route lifecycle correctly.

Do not leave a cleanup-capable router whose application callback always returns `undefined`.

Required:

- render function cleanup reaches the router;
- stale pending render cleanup is handled safely;
- cleanup never runs twice in a way that causes an exception;
- form reset/dialog cleanup cannot mutate a newly mounted route.

Remove the current required-password double-render shortcut if present. A hash navigation should produce one authoritative route render, not a manual render plus a second hashchange render.

---

# H-003 — Theme preference `system` must really follow the OS

Phase 1J frozen resolution is:

```text
1. valid local preference when present
2. otherwise configured application default
3. `system` resolves through prefers-color-scheme
```

Current behavior effectively does:

```text
if preference == system and configuredDefault is dark/light
    -> use configuredDefault
```

That means a user explicitly choosing **System** cannot follow the OS when the application default is Dark or Light.

Fix the semantics.

Required model:

```text
stored preference exists:
    preference = stored value
else:
    preference = configured default

resolved appearance:
    preference dark  -> dark
    preference light -> light
    preference system -> OS media query
```

The configured default chooses the initial preference only when no valid local preference exists. It must not override a later explicit `system` preference.

Add a regression covering:

```text
configured default = dark
stored/user preference = system
OS preference = light
resolved appearance = light
```

and OS change while preference remains system.

Do not add server-side preference persistence.

---

# H-004 — Jobs action-state correctness

## 4A. Detail loading leaves action controls visually disabled

Current `loadDetail()` sets `busyId`, draws the view, fetches detail, draws again while `busyId` is still set, and only afterward clears `busyId` without a final redraw.

Result: after opening a job, that job's View/Cancel/Retry controls can remain disabled in the rendered DOM even though the request has completed.

Fix so the final DOM always reflects the final non-busy state.

Add a browser/runtime regression if available.

## 4B. Retry availability must match server retry policy

Server retry requires:

```text
status in FAILED/CANCELLED
retryable == true
attempt_count < max_attempts
```

Frontend retry eligibility must use the same returned-state conditions.

Do not display an enabled Retry action when attempts are exhausted.

## 4C. Cancellation action must reflect `cancel_requested`

For a RUNNING job with:

```text
cancel_requested == true
```

a new Cancel action is no longer meaningful.

Hide/disable it and show the returned cancellation-requested state instead.

Queued jobs remain cancellable.

Server remains authoritative; frontend state checks are UX only.

---

# H-005 — A 503 readiness document is `not_ready`, not "unreachable"

`/health/ready` deliberately returns:

```text
200 -> ready
503 -> valid minimal not_ready HealthResponse
```

Current generic API parsing treats every 503 as an exception, so:

- login readiness can say "unavailable" when the server is actually reachable but not ready;
- Overview cannot display the actual `not_ready` readiness state.

Preserve generic error behavior for ordinary API endpoints, but make the dedicated readiness client understand the legitimate 503 readiness document.

Required:

```text
200 JSON HealthResponse -> return document
503 JSON HealthResponse with status=not_ready -> return document
network failure / malformed body / unexpected response -> safe ApiError
```

Do not treat arbitrary 503 JSON as readiness data without validating the minimal expected shape.

Then:

- Login indicator distinguishes `ready`, `not_ready`, and truly unavailable.
- Overview can render actual readiness status even when it is `not_ready`, provided its authenticated Jobs call succeeds.

No public readiness API change is required.

---

# H-006 — Required-password mobile escape path

Normal navigation must remain blocked while `must_change_password=true`.

However, on mobile the topbar Logout button is hidden and the required-password view has no logout control. This can trap the user in the password-change screen.

Add a clear secondary **Sign out** action inside the required-password view.

Requirements:

- uses existing CSRF-protected logout flow;
- does not expose normal navigation;
- does not weaken the required-password gate;
- works on mobile/desktop;
- avoids duplicate submission while logout is pending through the existing centralized logout protection.

No new backend route.

---

# 2. Preserve all Phase 1J strengths

Do not regress:

- CampaignSim / Powered by IPSP branding;
- dataset-agnostic copy;
- no reference marketing demo logic/data;
- Vanilla JS ES modules;
- no build system;
- no npm;
- no CDN;
- no external fonts/assets;
- dark/light semantic tokens;
- responsive shell;
- accessible navigation;
- safe DOM construction;
- no unsafe HTML sinks;
- identity only in memory;
- only `ipsp.theme` in localStorage;
- CSRF cookie access only in `api.js`;
- no session-token access;
- owner-only Jobs APIs;
- System Health endpoint remains authorization authority;
- no role-name Admin checks;
- no job-submission UI;
- no raw-log UI;
- no fake dataset/model/simulation features.

---

# 3. Scope lock

Do NOT add/change:

- ORM schema;
- Alembic migration;
- permission catalog;
- auth/session backend semantics;
- CSRF backend semantics;
- job state machine;
- job API routes;
- system-health API;
- user-preference persistence;
- project/dataset/model/simulation APIs;
- WebSocket/SSE;
- frontend framework;
- npm/package.json/node_modules;
- Python dependency;
- Phase 1K code.

Expected remains:

```text
Alembic head = 20260812_05
ORM tables = exactly 7
pyproject.toml unchanged
requirements.lock unchanged
```

---

# 4. Frontend security must remain strict

Production JS must continue to contain none of:

```text
innerHTML
outerHTML
insertAdjacentHTML
document.write
eval(
new Function
```

Only `theme.js` may use `localStorage`.

Only `api.js` may read `document.cookie`.

No auth/session/CSRF/job/health payload persistence.

No API/user value may become raw HTML.

No external resource URLs.

No role-name authorization.

---

# 5. Tests to add/strengthen

At minimum cover:

1. router has an explicit active-route cancellation/generation primitive;
2. view cleanup returned by application render path reaches router lifecycle;
3. stale async route result cannot win after later navigation;
4. Jobs dialog closes on route disposal;
5. System preference follows OS even with configured default dark/light;
6. Jobs detail completion restores controls;
7. exhausted-attempt FAILED/CANCELLED job has no Retry action;
8. RUNNING + `cancel_requested=true` has no new Cancel action;
9. readiness 503 minimal document is returned as `not_ready`;
10. network/unexpected readiness failure remains a safe error;
11. required-password view contains a sign-out action;
12. all existing frontend XSS/storage/cookie/CDN/contamination tests remain green.

Do not rely on timing sleeps for route-race tests.

---

# 6. Documentation

Update:

```text
docs/31_IMPLEMENTATION_PROGRESS.md
```

Add:

```text
Phase 1J.1 — Frontend Lifecycle & State Hardening
```

Record:

- stale async route protection;
- cleanup lifecycle;
- System theme correction;
- Jobs action-state correction;
- readiness 503 semantics;
- required-password mobile sign-out;
- no schema/dependency/backend-authority change;
- exact test/quality evidence.

Update README only if operational behavior documented there needs correction.

Do not mark Phase 1 complete.

Phase 1K remains next after independent review.

---

# 7. Mandatory verification

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
alembic current
alembic check
```

If the existing environment provides the same browser execution facility used in Phase 1J QA, rerun it for:

- rapid route change while request is pending;
- Jobs detail action restoration;
- required-password mobile sign-out;
- System theme with OS preference;
- readiness `not_ready` display.

Do not install Node/npm solely for verification.

Confirm:

```text
head = 20260812_05
7 ORM tables
no migration
no dependency change
no Phase 1K
```

---

# 8. Mandatory Codex final report

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Route lifecycle architecture
Explain:
- invalidation primitive;
- cleanup ownership;
- stale async result suppression;
- why old content cannot overwrite a later route.

## E. Cleanup wiring
Report Login/Jobs/Profile/required-password cleanup behavior and dialog disposal.

## F. Theme correction
Report configured-default vs stored preference vs System/OS resolution and regression evidence.

## G. Jobs state correction
Report:
- detail busy-state restoration;
- cancel eligibility;
- retry eligibility including attempts;
- server-authoritative mutation behavior.

## H. Readiness semantics
Report 200/503 valid document handling and true failure behavior.

## I. Required-password sign-out
Report mobile/desktop behavior and confirmation that normal navigation remains blocked.

## J. Security regression
Confirm unsafe-DOM/storage/cookie/session-token/CDN/role-name/contamination guards remain green.

## K. Prior-phase regression
Confirm Phase 1E through 1J functionality remains green.

## L. Tests
Exact passed/failed/skipped/warnings.

## M. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, diff check, Alembic heads/current/check, browser QA if available.

## N. Schema/dependency state
Confirm migration/schema/pyproject/lock unchanged.

## O. Runtime artifacts
Confirm no DB/WAL/SHM/log/browser profile/node_modules/build output/credential residue.

## P. Phase boundary
Confirm no Phase 1K work.

## Q. Git state
Final status and diff stat.

## R. Deviations / unresolved issues
If none: `None`

## S. Gate result

End exactly with:

`Phase 1J.1: PASS — Phase 1K ready for independent review`

or

`Phase 1J.1: FAIL — Phase 1K blocked`

Do not begin Phase 1K.
