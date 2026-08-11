# IPSP v1.0 — Phase 1A Codex Implementation Prompt
## Repository & Application Foundation

You are implementing IPSP v1.0 in the existing repository.

**Current project state**
- Phase 0: COMPLETE
- Phase 0.5: PASS
- Documentation Freeze: PASS
- Phase 1: READY
- This task is **Phase 1A / v0.1.0 — Repository + Application Skeleton**

This is the **first production-code implementation task**.

---

# 1. Governing rule

The frozen repository documentation is the implementation authority.

Do **not** redesign the architecture.
Do **not** introduce domain-specific assumptions.
Do **not** implement later-phase features early.

If a frozen specification is ambiguous or contradictory in a way that affects code, **stop and report the conflict instead of inventing a solution**.

---

# 2. Required reading before editing

Read completely, in this order:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/01_PROJECT_SPEC.md`
5. `docs/02_PRODUCT_REQUIREMENTS.md`
6. `docs/03_ARCHITECTURE.md`
7. `docs/04_PROJECT_STRUCTURE.md`
8. `docs/05_UI_UX_SPEC.md`
9. `docs/06_UI_DESIGN_SYSTEM.md`
10. `docs/18_SECURITY_RBAC_SPEC.md`
11. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
12. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
13. `docs/23_ERROR_HANDLING_SPEC.md`
14. `docs/24_JOB_PROCESSING_SPEC.md`
15. `docs/27_SQLITE_SCHEMA_SPEC.md`
16. `docs/28_REST_API_CONTRACT.md`
17. `docs/29_TEST_STRATEGY.md`
18. `docs/30_ACCEPTANCE_CRITERIA.md`
19. `docs/31_IMPLEMENTATION_PROGRESS.md`
20. `docs/32_DECISION_LOG.md`
21. `docs/34_CODING_STANDARDS.md`
22. `docs/35_CONFIGURATION_SPEC.md`
23. `docs/37_SYSTEM_HEALTH_SPEC.md`
24. `docs/40_ANTI_CONTAMINATION.md`
25. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`
26. `docs/PHASE_0_5_RECONCILIATION_REPORT.md`

Also inspect the canonical UI/reference assets already present in the repository.

Before writing code, establish the authoritative:
- package layout;
- database access model;
- route ownership;
- configuration ownership;
- error-handling boundary;
- logging/audit boundary;
- offline frontend policy;
- job-contract requirement;
- benchmark-isolation rule.

Do not create another architecture document unless a required implementation note genuinely belongs in an existing document.

---

# 3. Phase 1A objective

Create the **minimal production-ready repository and application foundation** on which later Phase 1 work packages will build.

Phase 1A must establish:

1. Python project/package skeleton.
2. FastAPI application factory and application bootstrap.
3. Canonical package/module boundaries from the frozen project structure.
4. Configuration bootstrap and environment loading foundation.
5. Central dependency/version declaration.
6. Central error-envelope scaffolding.
7. Request/trace context scaffolding.
8. Canonical API router registration structure.
9. Liveness and readiness endpoint skeletons.
10. Job-domain contracts/interfaces only.
11. Frontend file/directory foundation.
12. Shared dark/light design-token foundation.
13. Vendored-asset directory/policy scaffold.
14. Test bootstrap and smoke tests.
15. Tooling configuration for linting/type checking/testing.
16. Local development entry/run instructions.
17. Progress/decision documentation updates only where implementation actually changes project state.

This task is deliberately narrow.

---

# 4. Explicitly DO NOT implement in Phase 1A

Do NOT yet implement:

- full SQLAlchemy schema;
- Alembic business migrations;
- users/roles/permissions tables;
- authentication/login/logout;
- password hashing workflow;
- CSRF implementation;
- account lockout;
- RBAC enforcement;
- dataset upload;
- dataset profiling;
- Parquet conversion;
- semantic understanding;
- relationship inference;
- capability discovery;
- ML model training;
- simulation execution;
- Monte Carlo;
- SDV;
- LLM providers beyond an interface/stub only if required by the frozen structure;
- reporting/PDF/Excel;
- model registry;
- dataset manifests;
- benchmark-specific logic;
- campaign-specific UI;
- Redis;
- Celery;
- Docker orchestration unless an already-frozen spec explicitly requires a minimal placeholder now.

No demo business data.
No hardcoded marketing fields.
No fake simulator output.

---

# 5. Canonical implementation constraints

## 5.1 Python / backend

Use the frozen architecture.

Expected principles:

- Python 3.11+ compatible.
- FastAPI application.
- Uvicorn for local serving.
- SQLAlchemy 2.x synchronous control-plane architecture is the locked database model, but the actual business schema comes in later work packages.
- Do not use legacy `Session.query()`.
- Do not wrap synchronous DB work inside fake `async def`.
- API routes belong in the canonical `backend/ipsp/api/routes/` location.
- Pydantic API schemas stay separate from ORM entities.
- Domain/services must not raise FastAPI `HTTPException`; centralized API exception handling maps IPSP/domain exceptions to HTTP responses.
- Use timezone-aware UTC.
- No secrets in source code.
- No production secret auto-generation.

## 5.2 Dependency management

Use `pyproject.toml` as the authoritative direct-dependency/configuration file.

At implementation time:
- resolve current maintained compatible package versions;
- do not copy old architecture-document pins blindly;
- do not add `sqlite3` as a pip dependency;
- avoid unnecessary dependencies;
- configure reproducible dependency locking/constraints using the repository's selected Python workflow;
- record why any non-obvious dependency is required.

Phase 1A dependencies should remain minimal.

## 5.3 Frontend

Frontend remains:

- HTML5
- CSS3
- Vanilla JavaScript
- Plotly.js only when charts are actually needed

For Phase 1A:
- create the frontend foundation;
- create semantic design tokens;
- create dark theme tokens;
- create light theme tokens;
- create theme-switch/persistence scaffolding;
- create reusable base layout styles;
- preserve the canonical CampaignSim visual language;
- do not copy campaign-specific business controls into the production UI.

Do not use a runtime CDN.

Create/retain:

`frontend/assets/vendor/`

for explicitly versioned vendored browser libraries.

Do not add Plotly merely to satisfy the folder structure if Phase 1A does not yet use it.

## 5.4 Offline/local-first

The application foundation must boot without Internet access.

No runtime public CDN.
No automatic outbound model downloads.
No hidden telemetry introduced by application code.

Any future outbound behavior must go through the frozen outbound-policy architecture.

---

# 6. Suggested physical structure

Follow `docs/04_PROJECT_STRUCTURE.md` as authority.

Do not create duplicate ownership locations.

At minimum, create the portions required by Phase 1A, such as:

```text
backend/
└── ipsp/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   ├── router.py
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   └── health.py
    │   └── schemas/
    │       ├── __init__.py
    │       └── common.py
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    ├── observability/
    │   ├── __init__.py
    │   ├── context.py
    │   └── logging.py
    ├── errors/
    │   ├── __init__.py
    │   ├── exceptions.py
    │   └── handlers.py
    ├── jobs/
    │   ├── __init__.py
    │   ├── contracts.py
    │   └── enums.py
    ├── database/
    │   ├── __init__.py
    │   └── models/
    │       └── __init__.py
    └── security/
        └── __init__.py

frontend/
├── index.html
├── css/
│   ├── tokens.css
│   ├── base.css
│   ├── layout.css
│   ├── components.css
│   ├── theme-dark.css
│   ├── theme-light.css
│   └── responsive.css
├── js/
│   ├── app.js
│   ├── api.js
│   └── theme.js
└── assets/
    └── vendor/

tests/
├── conftest.py
├── unit/
└── integration/

database/
└── migrations/

config/

scripts/
```

This tree is illustrative only. If the frozen `04_PROJECT_STRUCTURE.md` differs, **the frozen file wins**.

Do not create empty directories/files solely for appearance if they serve no near-term purpose.

---

# 7. FastAPI foundation requirements

Implement an application factory rather than a monolithic global script.

Conceptual contract:

```python
def create_app(settings: Settings | None = None) -> FastAPI:
    ...
```

The factory should:

- construct FastAPI;
- register central exception handlers;
- register request/trace context middleware;
- register the canonical API router;
- expose liveness/readiness probes;
- configure safe development behavior;
- avoid constructing unavailable later-phase services.

Avoid global mutable singletons.

## Health behavior

Implement exactly the frozen routing semantics:

- `/health/live`
  - unversioned infrastructure probe;
  - confirms process/application is alive;
  - minimal safe response.

- `/health/ready`
  - unversioned infrastructure probe;
  - Phase 1A may initially validate configuration/application readiness only;
  - do not pretend database/storage dependencies are checked until those dependencies exist;
  - structure it so later readiness checks can be added.

Do NOT implement the rich authenticated Admin health page/endpoint yet unless the frozen Phase 1A scope explicitly requires only a placeholder contract.

Business/application APIs belong under `/api/v1`.

---

# 8. Central error foundation

Implement the common safe error infrastructure without prematurely creating every future subsystem error.

Use the subsystem taxonomy from `23_ERROR_HANDLING_SPEC.md`.

At minimum provide:

- a base IPSP exception;
- safe error response schema;
- stable error-code pattern;
- central FastAPI exception mapping;
- generic unexpected-error handling that does not expose stack traces or secrets.

Do not use ad-hoc route-level `HTTPException` for domain failures when an IPSP/domain exception is appropriate.

Tests must verify that unexpected errors do not expose raw stack traces.

---

# 9. Request / trace context foundation

Implement request correlation scaffolding consistent with `22_OBSERVABILITY_AUDIT_SPEC.md`.

At minimum:

- request ID;
- trace ID;
- context propagation available to logs;
- no raw session bearer tokens;
- safe structured log fields;
- timezone-aware UTC timestamps.

Full durable audit persistence comes later with database work.

Do not invent user/session fields before authentication exists.

---

# 10. Job contracts only

Create the frozen job abstraction contracts required by the foundation.

At minimum represent:

- `JobType`
- `JobStatus`
- `JobBackend`
- progress state
- cancellation contract
- retry/error contract

Do not yet implement:

- Redis;
- Celery;
- distributed workers;
- heavy execution;
- ML jobs.

If an in-process no-op/local placeholder is necessary for typing/tests, keep it minimal and clearly non-production for execution.

---

# 11. Configuration foundation

Implement the minimum settings model required to boot Phase 1A.

Examples of categories:
- environment;
- app name/version;
- debug flag;
- host/port if appropriate;
- control-plane database URL placeholder/default for local development only if required;
- data/artifact/log directories;
- outbound-policy defaults;
- theme/application defaults only if backend-owned.

Follow `35_CONFIGURATION_SPEC.md`.

Production-critical secrets must have no insecure generated default.

Do not implement remote LLM credentials yet.

Provide `.env.example` with placeholders only.
Do not create or commit a real `.env` containing secrets.

---

# 12. Frontend foundation

Create a real but minimal shell using the frozen visual system.

Required:
- IPSP/CampaignSim product shell according to frozen branding rules;
- no fake business metrics;
- no hardcoded campaign controls;
- accessible semantic HTML;
- responsive foundation;
- dark theme;
- light theme;
- theme switch;
- local preference persistence;
- clear loading/error/empty-state component styles where appropriate.

The frontend should be capable of loading as a static page and should not require Internet access.

Do not build the dataset onboarding or simulation workflows yet.

---

# 13. Tests required in Phase 1A

Create meaningful tests, not placeholder assertions.

At minimum verify:

## Backend
- app factory creates application;
- liveness returns expected safe response;
- readiness returns expected Phase 1A response;
- `/api/v1` router structure is mounted correctly where applicable;
- central error envelope works;
- unexpected exception does not expose stack trace;
- request/trace IDs are attached or propagated as designed;
- settings can load from environment;
- required production configuration fails safely where applicable;
- job enums/contracts are importable and internally valid.

## Architecture/conformance
- no benchmark-specific production terms in newly created core source where such a scan is feasible;
- no runtime CDN reference in production frontend files;
- no `Session.query(` in production code;
- no Streamlit imports;
- no JWT/python-jose browser-auth implementation;
- no hardcoded campaign simulator outputs.

## Frontend
If the project test strategy supports it without adding heavy tooling:
- validate critical static structure;
- verify both theme files/tokens exist;
- verify theme JS uses supported preference resolution.

Do not add a large frontend testing framework solely for Phase 1A.

---

# 14. Tooling / quality gates

Configure the frozen project-quality tooling.

At minimum run as applicable:

- tests;
- Ruff/lint;
- formatting check;
- type checking.

Do not declare success if a configured gate fails.

Warnings should be classified, not ignored.

---

# 15. Documentation updates after implementation

After code is complete and tests pass:

Update `docs/31_IMPLEMENTATION_PROGRESS.md` with the actual Phase 1A status.

Only update `docs/32_DECISION_LOG.md` if a real implementation decision was necessary that was not already frozen.

Do not rewrite architecture documents to rationalize implementation drift.

If implementation exposes a spec contradiction, report it instead.

---

# 16. Git discipline

Work on the current Phase 1 implementation branch.

Before editing:

```text
git status --short
```

The tree should be understood before modifications.

After implementation, show:

```text
git status --short
git diff --stat
```

Do not automatically push.
Do not rewrite history.
Do not commit generated secrets, virtual environments, caches, logs, local databases, or uploaded runtime data.

Ensure `.gitignore` covers appropriate local/runtime artifacts.

---

# 17. Phase 1A acceptance gate

Phase 1A is PASS only if:

- repository/package skeleton follows frozen architecture;
- FastAPI app factory works;
- liveness works;
- readiness foundation works honestly;
- API route ownership is canonical;
- central error envelope works;
- request/trace context foundation works;
- minimal configuration works;
- no insecure production secret defaults exist;
- job contracts exist without distributed-queue dependency;
- frontend shell exists;
- dark/light theme foundation works;
- no runtime CDN is required;
- tests pass;
- lint/type/format checks pass or any justified exception is reported;
- no benchmark-specific business logic appears in generic core;
- no later-phase functionality was prematurely implemented;
- documentation progress is updated accurately.

---

# 18. Mandatory final response

Do not just say "done".

Return:

## A. Files created
List every production/test/config/documentation file created.

## B. Files modified
List every existing file modified.

## C. Implementation summary
Explain what was actually implemented.

## D. Dependencies added
For each direct dependency:
- name;
- purpose;
- selected version/constraint;
- why required now.

## E. Commands executed
Include relevant:
- install/sync;
- test;
- lint;
- format;
- type-check;
- run/smoke commands.

## F. Test results
Give exact pass/fail counts.

## G. Quality-gate results
Ruff / formatter / type checker / other configured gates.

## H. Architecture conformance checks
Explicitly report:
- benchmark contamination scan;
- Streamlit scan;
- legacy `Session.query()` scan;
- runtime CDN scan;
- hardcoded campaign/demo output scan.

## I. Git state
Show:
- `git status --short`
- `git diff --stat`

## J. Deviations / unresolved issues
If none, say `None`.

## K. Gate result
End exactly with one of:

`Phase 1A: PASS — ready for Phase 1B review`

or

`Phase 1A: FAIL — Phase 1B blocked`

Do not begin Phase 1B in this run.
