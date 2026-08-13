# IPSP v1.0 — Phase 1J Codex Implementation Prompt
## Production Frontend Design-System Expansion + Authenticated Foundation Workspace

**Repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** `e0dedf671b390302351a041b47bc2b63acc1c3f7`

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
- Phase 1J: AUTHORIZED
- Application version remains `v0.1.0`

This task is **Phase 1J only**. It is the first substantial production UI phase. It must establish the reusable frontend design system and a real authenticated workspace over **only the foundation capabilities already implemented**.

Do not begin Phase 1K integration/security acceptance, Phase 1L audit, ingestion, profiling, semantic discovery, capability/model discovery, simulation, reports, LLM providers, user-management APIs, backup execution, or the full v0.7 dynamic frontend.

---

# 1. Canonical visual contract

Official reference:

`reference/Campaign_simulator_UI.html`

Use it as a **visual/design reference only**. Preserve its visual language:

- dark layered surfaces;
- indigo/violet primary accents;
- restrained ambient glow/grid treatment;
- compact cards;
- sticky top navigation;
- metric cards;
- selectable cards;
- badges;
- alerts;
- progress;
- tabs;
- stepper styling;
- compact tables;
- heading/body/mono typography roles;
- responsive grids.

Build a complete light theme using the same semantic token system.

Do **not** copy sample campaign business logic into production. Prohibited production concepts include fixed budgets, objectives, channel lists, audience assumptions, historical campaign similarity, ROAS, CPA, CTR, reach, ad fatigue, creative quality, campaign scenarios, fake historical matches, sample brands, sample dates/locations, or static simulation results.

The only marketing-adjacent item explicitly allowed is the frozen initial branding:

`CampaignSim / Powered by IPSP`

Branding does not make the product marketing-specific. The underlying product and UI must remain dataset-agnostic.

---

# 2. Read before editing

Read completely:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/02_PRODUCT_REQUIREMENTS.md`
5. `docs/03_ARCHITECTURE.md`
6. `docs/04_PROJECT_STRUCTURE.md`
7. `docs/05_UI_UX_SPEC.md`
8. `docs/06_UI_DESIGN_SYSTEM.md`
9. `docs/18_SECURITY_RBAC_SPEC.md`
10. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
11. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
12. `docs/23_ERROR_HANDLING_SPEC.md`
13. `docs/28_REST_API_CONTRACT.md`
14. `docs/29_TEST_STRATEGY.md`
15. `docs/30_ACCEPTANCE_CRITERIA.md`
16. `docs/31_IMPLEMENTATION_PROGRESS.md`
17. `docs/34_CODING_STANDARDS.md`
18. `docs/35_CONFIGURATION_SPEC.md`
19. `docs/37_SYSTEM_HEALTH_SPEC.md`
20. `docs/40_ANTI_CONTAMINATION.md`
21. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`
22. `reference/Campaign_simulator_UI.html`

Inspect all current frontend files:

- `frontend/index.html`
- `frontend/css/*`
- `frontend/js/*`
- `frontend/assets/vendor/*`

Inspect currently usable backend APIs and schemas:

- `backend/ipsp/api/routes/root.py`
- `backend/ipsp/api/routes/auth.py`
- `backend/ipsp/api/routes/jobs.py`
- `backend/ipsp/api/routes/admin_system.py`
- `backend/ipsp/api/schemas/common.py`
- `backend/ipsp/api/schemas/auth.py`
- `backend/ipsp/api/schemas/jobs.py`
- `backend/ipsp/api/schemas/system_health.py`
- `backend/ipsp/auth/cookies.py`
- `backend/ipsp/config/settings.py`
- `backend/ipsp/main.py`

Inspect current auth/jobs/health/frontend architecture tests.

Before editing:

```text
git status --short
git rev-parse HEAD
```

Start from a clean tracked worktree except known user-owned prompt files.

---

# 3. Technology lock

Production frontend remains:

```text
HTML5
CSS3
Vanilla JavaScript ES modules
```

Do NOT add React, Vue, Angular, Svelte, Next.js, Nuxt, Vite build/runtime requirements, TypeScript build tooling, npm dependencies, jQuery, Bootstrap, Tailwind, Streamlit, public CDN assets, external fonts, external icon libraries, or browser analytics/telemetry.

Use same-origin FastAPI APIs. The existing `StaticFiles` hosting model remains valid.

No new Python dependency is expected.

---

# 4. Phase 1J deliverables

Implement:

1. expanded reusable design tokens;
2. complete dark and light themes;
3. responsive application shell;
4. accessible navigation;
5. Vanilla-JS client-side hash routing;
6. robust same-origin API client;
7. login/session bootstrap;
8. required-password-change flow;
9. authenticated Overview page;
10. current-user Jobs page;
11. Profile page;
12. change-password UI;
13. authorized System Health UI;
14. loading/empty/error/permission states;
15. System / Dark / Light theme preference;
16. responsive/mobile behavior;
17. print-safe diagnostic/job styling;
18. no CDN/runtime external asset dependency;
19. frontend security/anti-contamination tests;
20. accurate documentation.

Every visible operational value must come from an implemented API or be explicitly labelled unavailable/not implemented.

No fake dashboards.

---

# 5. Routing model

Use a small **hash router** so direct static hosting continues to work without a backend SPA catch-all.

Required routes:

```text
#/login
#/overview
#/jobs
#/profile
#/admin/system
```

Unknown route -> safe not-found state.

On route change:

- update active navigation;
- update document title;
- move focus to main heading/content appropriately;
- clean up page-specific listeners/timers;
- preserve theme;
- never preserve sensitive form values.

Do not use server-history routes requiring catch-all rewriting.

---

# 6. Login and session flow

Build a polished login page in the canonical visual language.

Required:

- CampaignSim / Powered by IPSP branding;
- username field;
- password field;
- submit button;
- safe loading/error state;
- optional minimal readiness indicator;
- real labels and keyboard accessibility;
- appropriate autocomplete attributes;
- no demo credentials;
- no signup/forgot-password flows because those APIs do not exist.

Login uses:

`POST /api/v1/auth/login`

After success:

- keep identity only in application memory;
- never store session token/password;
- navigate to overview unless `must_change_password=true`.

Bootstrap authenticated state using:

`GET /api/v1/auth/me`

On later API 401:

- clear in-memory identity;
- route to login;
- show a safe session-expired state.

Logout uses the existing CSRF-protected route and then clears in-memory state.

---

# 7. Required password change

If `identity.must_change_password == true`, block normal navigation and show required password change.

Use:

`POST /api/v1/auth/change-password`

Fields:

- current password;
- new password;
- confirm new password.

Frontend may validate only confirmation mismatch. Do not invent password rules beyond backend validation.

After successful password change, the backend invalidates the current session; return to login with a success message.

Never persist password fields.

---

# 8. Authenticated shell

Build a reusable shell containing:

```text
sticky topbar
responsive desktop navigation rail/sidebar
main content
mobile navigation
footer/status area where useful
```

Topbar:

- CampaignSim;
- Powered by IPSP;
- page context/title;
- theme control;
- current user display identity;
- logout.

Navigation:

```text
Overview
Jobs
Profile
System Health
```

The System Health destination is permission protected by the backend. Frontend must never infer access from role name.

Do not add functional navigation to projects/datasets/models/simulations because those APIs do not exist yet.

A clearly disabled roadmap panel on Overview is acceptable.

---

# 9. Overview

Overview is a truthful foundation workspace, not a business-performance dashboard.

Use actual data from:

```text
GET /api/v1
GET /health/ready
GET /api/v1/auth/me
GET /api/v1/jobs?limit=<bounded>
```

Recommended sections:

### Platform readiness
Actual readiness state plus safe active/deferred check counts.

### Session
Display only safe identity/session fields:

- display name;
- username;
- role name as descriptive text only;
- session expiration;
- must-change-password state.

### Recent jobs
Small actual recent list. Do not call a limited list a complete historical KPI.

### Implemented foundation capabilities
Static statements only for features that really exist, e.g. secure sessions, permission-based access, observability/audit, local jobs, system health.

### Later milestones
Projects, datasets, semantics, models and simulation may appear only as clearly disabled/not-yet-implemented roadmap states. No fake counts.

---

# 10. Jobs UI

Use current owner-only routes:

```text
GET  /api/v1/jobs
GET  /api/v1/jobs/{job_id}
POST /api/v1/jobs/{job_id}/cancel
POST /api/v1/jobs/{job_id}/retry
```

Render:

- job type;
- status;
- progress;
- phase/message;
- timestamps;
- attempt/max attempts;
- retryability;
- cancellation request state;
- safe error code/message;
- safe artifact references as text only.

Support exact current states:

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

Use status badges, progress bars, compact responsive table/list, empty/loading/error states.

Cancel/retry must:

- use CSRF;
- be available only when server-returned state supports the action;
- prevent duplicate clicks while pending;
- render the returned server snapshot after success;
- use a clear confirmation interaction for cancellation.

Do not implement a job-submit/create UI.

Provide explicit refresh. Aggressive polling is unnecessary.

---

# 11. Profile UI

Display only current identity/session data:

- display name;
- username;
- email when present;
- role name as descriptive text only;
- session expiry;
- theme preference.

Do not create editable username/email/profile fields because no API exists.

Include change-password and logout actions.

Do not fabricate permission lists.

---

# 12. System Health UI

Use:

`GET /api/v1/admin/system/health`

Render actual Phase 1I groups:

- overall health;
- readiness;
- SQLite;
- storage;
- job worker;
- local LLM;
- remote LLM;
- outbound policy;
- model artifacts;
- backup;
- recent critical errors;
- runtime CPU/memory.

Permission behavior:

```text
401 -> resolve session/login
403 -> dedicated permission state
200 -> diagnostics
```

Do not use role-name checks such as `role_name == "Admin"`.

Map current health states honestly:

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

Never map `not_implemented` to healthy.

Use text/icon/shape in addition to color.

Do not reconstruct absolute paths from safe `display_path`.

No raw-log viewer in this phase.

---

# 13. Safe browser bootstrap config

The static frontend must not hardcode configurable CSRF browser names.

Current settings include:

- `default_theme`;
- `csrf_cookie_name`;
- `csrf_header_name`.

Preferred minimal solution: extend the existing public versioned root response `GET /api/v1` with a typed nested object such as:

```json
{
  "name": "IPSP",
  "version": "0.1.0",
  "status": "foundation",
  "browser": {
    "default_theme": "system",
    "csrf_cookie_name": "ipsp_csrf",
    "csrf_header_name": "X-CSRF-Token"
  }
}
```

Exact model naming may differ.

Constraints:

- no session token/value;
- no CSRF token/value;
- do not expose the session cookie name unless genuinely required;
- no secret/config dump;
- no DB URL;
- keep response public and safe;
- update root response tests;
- test custom safe CSRF names/default theme, not just defaults.

Do not add another route family if the root response is sufficient.

---

# 14. API client

Expand `frontend/js/api.js` into the canonical same-origin browser client.

Required:

- `credentials: "same-origin"`;
- relative same-origin URLs only;
- JSON Accept;
- Content-Type only when a body exists;
- 204 support;
- safe parsed error object;
- no raw response dumps;
- no console logging of payloads/secrets;
- configured CSRF cookie/header names from browser bootstrap;
- read CSRF cookie only immediately for state-changing calls;
- never read HttpOnly session cookie;
- no CSRF for GET/login;
- CSRF for logout/change-password/cancel/retry.

Recommended functions:

```text
getBrowserConfig
getReadiness
login
getCurrentUser
logout
changePassword
listJobs
getJob
cancelJob
retryJob
getSystemHealth
```

Do not create an arbitrary client surface that accepts untrusted remote URLs.

---

# 15. Hard frontend security rules

Production JS must not use API/user values through:

```text
innerHTML
outerHTML
insertAdjacentHTML
document.write
eval
new Function
```

Use safe DOM construction:

```text
createElement
textContent
controlled setAttribute
```

Do not use inline `onclick` handlers; use `addEventListener`.

### Storage

LocalStorage may contain only visual preference such as `ipsp.theme`.

Never persist:

- username/display name/email/role;
- permissions;
- identity/session data;
- session token;
- CSRF token;
- passwords;
- job data;
- health data.

Do not use localStorage as an authorization source.

### Cookies

Only the canonical API module may access `document.cookie`, and only for the configured CSRF cookie.

### URLs/artifacts

Do not create links from API-returned artifact references. Display them as text until a safe download API exists.

No `javascript:` URLs.

### Console

Do not log API responses, identity, passwords, cookies, CSRF or job data.

---

# 16. Theme system

Preferences:

```text
system
dark
light
```

Persist only `ipsp.theme` locally.

Resolution:

1. valid local preference when present;
2. otherwise configured application default;
3. `system` resolves via `prefers-color-scheme`.

Requirements:

- visible three-state preference UI;
- theme control accessible from topbar/profile;
- OS changes update UI when preference is system;
- dark/light files expose the same semantic variable set;
- components depend on semantic tokens rather than theme-specific copies;
- update `color-scheme` appropriately;
- no server-side user-preference persistence because that schema/API does not exist.

---

# 17. Design tokens and CSS modules

Expand semantic tokens for:

- background/surface levels;
- text/muted text;
- primary/secondary accent;
- success/warning/danger/info;
- borders;
- input/focus;
- overlays;
- heading/body/mono typography roles;
- spacing;
- radii;
- shadows/glows;
- motion/easing;
- content/sidebar widths.

Dark theme should remain recognizably based on the canonical near-black + indigo/violet reference. Light theme must be purpose-designed, not simply inverted.

No remote fonts. Use system/local fallback stacks while preserving heading/body/mono roles.

Evolve CSS toward cohesive modules such as:

```text
tokens.css
theme-dark.css
theme-light.css
base.css
layout.css
navigation.css
cards.css
forms.css
buttons.css
tables.css
alerts.css
progress.css
admin.css
responsive.css
print.css
```

Do not create empty files just to satisfy the list. Avoid duplicate component rules.

Core component modules should use semantic variables instead of scattered raw color literals.

---

# 18. Reusable components

Establish reusable styling/behavior for:

- Card;
- Metric card;
- Selectable card;
- Badge;
- Alert;
- Button/icon button;
- Form group/text/select;
- Theme selector;
- Navigation item;
- Empty/loading/error/permission states;
- Progress;
- Table;
- Tabs;
- Stepper;
- confirmation dialog;
- trust/status meter.

Do not bind components to marketing fields.

---

# 19. Visual structure

The application should visibly descend from the reference rather than look like generic unstyled forms.

Use:

- restrained background grid;
- indigo/violet ambient glow;
- optional secondary teal/violet glow;
- compact 10–14px radius cards;
- subtle borders;
- heading/body/mono hierarchy;
- small status badges;
- professional progress and table treatments.

Do not overuse glow.

User-facing branding:

```text
CampaignSim
Powered by IPSP
Intelligent Predictive Simulation Platform
```

Operational copy must remain generic, e.g. "Platform workspace", "Recent jobs", "System health".

---

# 20. Responsive and accessibility

Target practical behavior around:

```text
desktop >= 1100
tablet 768–1099
mobile < 768
small mobile < 480
```

Required:

- desktop sidebar becomes mobile drawer/collapsible navigation;
- no page-level horizontal overflow;
- tables remain usable with responsive wrapper/card adaptation;
- forms become single column where necessary;
- cards/health groups reflow;
- dialogs fit viewport;
- long IDs/timestamps wrap safely;
- useful touch-target sizes.

Accessibility:

- semantic header/nav/main;
- skip link;
- real buttons/links;
- associated labels;
- visible keyboard focus;
- `aria-current` on active nav;
- expanded state for mobile nav;
- route-change focus management;
- `aria-live` where useful;
- status not color-only;
- reduced-motion support;
- accessible confirmation behavior.

Do not use clickable divs as controls.

---

# 21. Motion and print

Keep transitions restrained, roughly 140–250 ms. No distracting continuous animation.

Respect:

`prefers-reduced-motion: reduce`

Add `print.css` for readable Jobs/System Health output:

- white/high-contrast print background;
- hide navigation/theme/logout/action controls;
- remove ambient glow/grid;
- avoid clipped cards/tables.

Do not implement PDF export.

---

# 22. Offline/runtime asset policy

Production UI must contain no runtime external browser asset dependency.

Ban:

- Google Fonts;
- fonts.gstatic.com;
- unpkg;
- jsdelivr;
- cdnjs;
- external Plotly;
- external icon/font CDNs.

No browser network call is required except same-origin IPSP APIs/health probes.

Do not vendor Plotly merely for this phase; no current foundation page needs charts.

Keep `frontend/assets/vendor/README.md` accurate.

---

# 23. Error/loading/concurrency UX

Create reusable safe error presentation.

Special handling:

```text
401 -> session/login
403 -> permission state
404 job -> not-found state
5xx -> generic safe error
```

Use backend safe error code/message when appropriate. Do not blindly render error `details`.

Prevent double mutations during login/logout/change-password/cancel/retry/refresh actions.

Server state is authoritative. Do not optimistically mark a job terminal before server confirmation.

---

# 24. Dates and IDs

API timestamps are UTC-aware. Display in browser local timezone using `Intl.DateTimeFormat`, while retaining machine-safe UTC in `datetime`/title where useful.

Do not assume a fixed timezone.

Use mono/wrapping for long IDs. Artifact refs remain text only.

---

# 25. Minimal backend scope permitted

Allowed backend changes are limited to static-frontend support:

- safe browser bootstrap fields on `/api/v1`;
- associated Pydantic schema/root mapping;
- associated tests.

Do NOT add:

- tables/migrations;
- permissions;
- user preference persistence;
- projects/datasets APIs;
- admin user APIs;
- new health APIs;
- job submission route;
- server templates;
- WebSockets/SSE;
- fake dashboard APIs.

Existing API behavior must remain compatible.

---

# 26. JS module structure

Prefer cohesive ES modules, for example:

```text
frontend/js/app.js
frontend/js/api.js
frontend/js/theme.js
frontend/js/router.js
frontend/js/state.js
frontend/js/dom.js
frontend/js/components.js
frontend/js/views/login.js
frontend/js/views/overview.js
frontend/js/views/jobs.js
frontend/js/views/profile.js
frontend/js/views/system-health.js
frontend/js/views/not-found.js
```

Exact split may vary.

Avoid one enormous `app.js`, circular imports, globals on `window`, inline events, and orphaned timers/listeners.

---

# 27. HTML shell

Evolve `frontend/index.html` into the static shell host.

Required:

- correct metadata;
- local CSS only;
- local ES module only;
- skip link;
- app/root container;
- accessible no-JS message;
- decorative ambient elements marked appropriately;
- no sample reference business content;
- no inline `onclick`;
- no external preconnect/font/script/style.

If JS fails, the initial document must remain safe and understandable.

---

# 28. Tests — design/theme structure

Add pytest static/architecture checks for production frontend.

At minimum:

- index is served at `/`;
- known CSS/JS assets are served;
- API/health routes are not shadowed by static hosting;
- no external resource tags;
- skip link/semantic app shell exists;
- no inline onclick;
- reduced-motion rule exists;
- print stylesheet exists;
- dark/light theme variable sets match;
- only theme module uses localStorage;
- no sessionStorage unless explicitly justified (prefer none).

Use Python standard library where possible; do not add BeautifulSoup solely for these tests.

---

# 29. Tests — frontend security

Add architecture scans proving production JS contains none of:

```text
.innerHTML
.outerHTML
insertAdjacentHTML
document.write
eval(
new Function
```

Only the canonical API client may access `document.cookie`.

No session-token access exists in JS.

No frontend authorization logic checks `Admin` role name.

No React/Vue/Angular/Svelte/jQuery/Bootstrap/Tailwind runtime/Streamlit.

No external runtime browser URLs.

Add XSS regression markers such as:

```text
<img src=x onerror=alert(1)>
<script>DO_NOT_EXECUTE</script>
"><svg/onload=alert(1)>
```

Do not execute payloads; prove API/user strings flow through safe text DOM construction and no dangerous sink exists.

---

# 30. Tests — anti-contamination

Production frontend must not contain reference demo strings/concepts such as:

```text
Summer Acquisition
ClimateWear
Target ROAS
Historical similarity
Search + Social
ad fatigue
ROAS
CPA
CTR
BF1
BF2
BF3
BF4
BF5
BF6
BF7
BF8
```

Do not scan `reference/` for this assertion.

`CampaignSim` is allowed only as branding.

---

# 31. Tests — browser bootstrap/auth contract

Test custom safe settings, not only defaults.

`GET /api/v1` must preserve name/version/status and return safe browser fields for configured default theme and CSRF cookie/header names.

Assert response contains no:

- session token/value;
- CSRF token/value;
- password;
- secret;
- DB URL;
- environment dump.

Add static/client-contract tests proving:

- login sends no CSRF;
- logout uses CSRF;
- change password uses CSRF;
- cancel/retry use CSRF;
- GET requests do not require mutation CSRF;
- CSRF names originate from browser config rather than duplicated hardcoded constants;
- session token is never referenced by JS.

Do not weaken backend auth tests.

---

# 32. Tests — Jobs/System Health UI contracts

Jobs UI must explicitly handle current status vocabulary only:

```text
QUEUED
RUNNING
SUCCEEDED
FAILED
CANCELLED
```

Ensure no create/submit-job UI exists.

System Health UI must explicitly handle all current Phase 1I component-state strings and rely on 403/200 rather than role-name authority.

Public health probes must not be used as a substitute for Admin rich health.

---

# 33. README/documentation cleanup

The current README top still has stale Phase 1B-era implementation wording. Correct it during Phase 1J.

Describe the implemented v0.1 foundation accurately at a high level:

- configuration/secrets/outbound;
- SQLite/Alembic;
- authentication/session/CSRF;
- RBAC;
- observability/audit;
- jobs/local worker;
- system health;
- frontend foundation.

Do not claim ingestion, semantics, ML, simulation, LLMs or full dynamic v0.7 UI are complete.

Keep the local-worker single-process constraint.

If needed for actual browser login on plain HTTP localhost, document the existing development-only `cookie_secure` override without weakening production HTTPS requirements.

Update:

- `README.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Record:

`Phase 1J — Frontend Design-System Expansion`

Phase 1K remains next. Do not mark Phase 1 complete.

---

# 34. Schema/dependency lock

Expected after Phase 1J:

```text
Alembic head = 20260812_05
ORM tables = exactly 7
new migration = none
pyproject.toml = unchanged
requirements.lock = unchanged
package.json = absent
node_modules = absent
```

No new Python or npm dependency.

If a dependency appears necessary, stop and report rather than adding it.

---

# 35. Preserve prior security behavior

All prior protections remain mandatory:

- Argon2id;
- timing equalization;
- opaque hashed server sessions;
- HttpOnly session cookie;
- CSRF;
- lockout;
- fixation resistance;
- password-change invalidation;
- RolePermission-only authorization;
- no Admin-name bypass;
- audit privacy;
- structured logging;
- ContextVar isolation;
- job lifecycle/recovery;
- atomic worker authority;
- liveness/readiness/Admin-health separation.

The frontend consumes these controls; it does not reproduce authority client-side.

---

# 36. Visual acceptance target

The completed pages should unmistakably look like a coherent descendant of the canonical HTML, not a generic browser form.

Expected visible qualities:

- near-black layered dark identity;
- indigo/violet accent;
- subtle grid/ambient glow;
- compact topbar/sidebar;
- professional cards;
- mono metrics/status text;
- small badges;
- clean forms/tables/progress;
- polished loading/empty/error/permission states;
- intentionally designed light theme.

Do not sacrifice readability for effects.

---

# 37. Quality gates

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

Expected head: `20260812_05`.

If Node is already installed, an optional JS syntax check is useful, but do **not** install Node/npm or make it a project dependency for this phase.

Do not mutate the default developer database.

---

# 38. Runtime artifact audit

Before final report ensure there is no unintended residue:

- test DB/WAL/SHM;
- runtime logs/JSONL;
- browser profiles;
- cookie/storage dumps;
- screenshots unless explicitly intended and reviewed;
- credentials/tokens;
- archives;
- node_modules/npm cache;
- new venv;
- `dist/` build output.

Frontend is source-served; do not introduce a build pipeline.

---

# 39. Phase 1J acceptance gate

PASS only if all are true.

### Visual system
- recognizable canonical design lineage;
- complete semantic dark/light themes;
- System/Dark/Light preference;
- responsive/accessibility foundations;
- no visually unrelated mini-app.

### Authentication
- login;
- `/auth/me` bootstrap;
- required password change;
- logout;
- no auth storage;
- correct CSRF.

### Workspace
- truthful Overview;
- real current-user Jobs;
- Profile;
- authorized System Health;
- no fake domain functionality.

### Security
- no unsafe DOM sinks;
- no role-name authorization;
- no session-token access;
- configured CSRF cookie/header usage;
- no external runtime assets;
- no secret logging/storage.

### Anti-contamination
- no copied marketing demo behavior/data;
- CampaignSim only as branding;
- no fixed ROAS/CPA/CTR/channel assumptions.

### Architecture
- Vanilla JS only;
- no frontend build/framework dependency;
- no schema/migration/dependency change;
- no Phase 1K+ implementation.

### Quality
- full pytest green;
- frontend security/architecture regressions green;
- prior auth/jobs/health regressions green;
- Ruff/mypy/compile/pip/diff/Alembic green.

---

# 40. Mandatory Codex final report

Return every section.

## A. Starting state
SHA, branch, initial git status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. UI architecture
Routing model, JS modules, CSS ownership, shell structure, no framework/build tool.

## E. Canonical visual reference
Visual principles extracted and demo campaign concepts deliberately excluded.

## F. Theme system
Token families, dark/light palettes, System/Dark/Light resolution, local persistence, reduced motion.

## G. Browser bootstrap config
API shape, CSRF names, default theme, privacy evidence.

## H. API client/security
Same-origin credentials, 204 handling, safe errors, CSRF, cookie/storage boundaries, unsafe-DOM prohibition.

## I. Authentication UI
Login, `/me`, required password change, logout, 401 behavior.

## J. Overview
Exact real API sources and explicit later-milestone disabled states.

## K. Jobs UI
List/details/status/progress/cancel/retry/refresh/states and confirmation there is no submission UI.

## L. Profile
Identity/session fields, change password, theme, unsupported fields kept non-editable.

## M. System Health UI
Rendered groups, permission behavior, status mapping, no role-name authority.

## N. Responsive/accessibility
Desktop/tablet/mobile, focus/keyboard/forms/reduced-motion/status semantics.

## O. Offline/browser assets
No CDN/fonts/scripts/vendor dependency added.

## P. Anti-contamination
Exact demo concepts searched/blocked and CampaignSim branding-only confirmation.

## Q. Frontend security evidence
No unsafe DOM sinks, no auth localStorage, only theme storage, no session-token access, no unsafe artifact links/API HTML rendering.

## R. README/documentation
Stale Phase 1B status corrected and current foundation accurately described.

## S. Prior-phase regression
Confirm Phase 1E through Phase 1I remain green.

## T. Tests
Exact passed/failed/skipped/warnings.

## U. Quality gates
Compileall, Ruff lint/format, strict mypy, pip check, diff check, Alembic heads/current/check, optional pre-existing Node syntax check if run.

## V. Architecture/conformance
Report seven ORM tables, head `20260812_05`, no migration, no route shadowing, no frontend framework/npm/CDN/Streamlit/network drift, no async DB/Redis/Celery, no domain contamination, backend static-message guard green.

## W. Dependency/schema state
`pyproject.toml`, lock, migration/schema changes. Expected none.

## X. Runtime artifacts
Logs/DB/WAL/SHM/browser profile/node_modules/build output/credentials/archives/venv residue.

## Y. Git state
Final status and diff stat.

## Z. Deviations / unresolved issues
If none: `None`.

## AA. Gate result

End exactly with one:

`Phase 1J: PASS — ready for independent review before Phase 1K`

or

`Phase 1J: FAIL — Phase 1K blocked`

Do not begin Phase 1K.
