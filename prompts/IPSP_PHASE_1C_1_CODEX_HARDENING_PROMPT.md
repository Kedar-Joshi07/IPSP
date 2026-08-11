# IPSP v1.0 — Phase 1C.1 Codex Hardening Prompt
## SQLite/Readiness/Privacy/Conformance Corrections Before Phase 1D

You are working in the existing IPSP repository after the Phase 1C implementation.

**Repository:** `Kedar-Joshi07/IPSP`
**Required starting point:** commit `bbef294c4a41a645f263b92b03983e00f1c8bd73` or a direct descendant containing no unreviewed Phase 1D work.

Current independent review status:
- Phase 1C implementation is structurally strong.
- Phase 1D remains BLOCKED pending this narrow Phase 1C.1 hardening pass.
- Do not redesign the database layer.
- Do not add any Phase 1D business/security ORM tables.
- Do not implement authentication/RBAC.
- Do not add Streamlit, React, Vue, Angular, or any frontend framework.
- Frontend remains HTML + CSS + Vanilla JS; backend remains Python/FastAPI.

This prompt corrects specific issues found during independent source review. Make no unrelated production changes.

# 1. Read first

Read:
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- current Phase 1C database/config/readiness/tests

Before editing:

```text
git status --short
git rev-parse HEAD
```

Preserve unrelated user-owned files.

# H-001 — Readiness failures must use HTTP 503

Current `/health/ready` returns HTTP 200 even when the body says `not_ready`.

Required:
- ready -> HTTP 200
- not_ready -> HTTP 503 Service Unavailable
- `/health/live` remains HTTP 200 and database-independent

Keep the same minimal safe `HealthResponse` body. Do not raise a domain exception merely to produce 503.

Tests:
- healthy ready -> 200
- migration-required -> 503
- unavailable DB -> 503
- liveness -> 200 even when readiness fails

# H-002 — SQLAlchemy SQL logging must hide bound parameters

Current engine passes `echo=settings.echo` without forcing parameter hiding.

Required:
- configure SQLAlchemy engine with `hide_parameters=True`
- this is not user-disableable in v0.1.0
- database echo may remain a diagnostic flag
- ordinary SQLAlchemy INFO logging and StatementError stringification must not expose bound values
- do not manually interpolate values into SQL logging

Add a security regression test using marker:

`DO_NOT_LEAK_DATABASE_PARAMETER`

with `echo=True` and a parameterized statement. The marker must not appear in captured logging/output/error text.

# H-003 — Deterministic repository-local default SQLite location

Current default `sqlite:///./ipsp.db` is CWD-relative.

Required:
- default DB target is repository-local, preferably `<repo>/database/ipsp.db`
- default must not depend on current working directory
- construct URL robustly for Windows/POSIX, preferably using SQLAlchemy URL utilities
- explicit `IPSP_DATABASE__URL` still overrides
- no DB file committed

`.env.example` must not accidentally replace the deterministic default with a CWD-relative override when copied. Prefer documenting the URL override as a commented example.

Tests:
- no-env default points to repository `database/ipsp.db`
- changing cwd does not change default target
- explicit environment override works

# H-004 — Restrict SQLite driver to synchronous stdlib forms

Current validation accepts any URL whose backend name is `sqlite`, which can let async/unfrozen SQLite driver forms through validation.

Accept only intended synchronous forms such as:
- `sqlite:///...`
- `sqlite+pysqlite:///...`

Reject at minimum:
- `sqlite+aiosqlite:///...`
- non-SQLite backends
- credential/host-bearing SQLite URLs

Do not install a new driver.

Add explicit `sqlite+aiosqlite` rejection test.

# H-005 — Readiness must verify FK enforcement

Current engine enables `PRAGMA foreign_keys=ON`, but readiness does not explicitly verify it.

Required:
- readiness queries `PRAGMA foreign_keys`
- require value `1`
- if disabled -> `not_ready`
- use stable safe error code such as `SYS-DATABASE-FK-DISABLED`
- expose no path/URL/raw exception

Tests:
- normal IPSP engine -> FK readiness passes
- engine/connection without FK enforcement -> readiness fails safely
- failure returns HTTP 503

# H-006 — Migration state must fail safely for multiple/unexpected heads

Keep Phase 1C linear-history invariant, but use multi-head-capable inspection so malformed/branched state is controlled.

Preferred:
1. inspect script heads with multi-head API
2. require exactly one script head
3. inspect DB current heads with multi-head API
4. zero DB heads before migration is valid but `at_head=False`
5. one matching head -> `at_head=True`
6. multiple unexpected script or DB heads -> safe `MigrationStateError`
7. readiness converts that to safe `not_ready`, not raw 500

Do not redesign future branching support.

Add tests for one expected head, unmigrated DB, correct head, and unexpected multiple-head state where practical.

# H-007 — Complete Phase 1C conformance/FK tests

Extend automated architecture tests to guard against:
- Streamlit
- React/Vue/Angular
- `Session.query(`
- `AsyncSession`
- `create_async_engine`
- `aiosqlite`
- production `metadata.create_all` / `.create_all(`
- duplicate `DeclarativeBase`
- duplicate/package-local Alembic roots
- premature Phase-1C business ORM table declarations
- runtime CDN
- JWT/python-jose
- outbound HTTP implementation
- Redis/Celery

Document the Phase-1C-only no-business-table guard so it can be evolved in Phase 1D.

Strengthen FK tests:
- verify `PRAGMA foreign_keys=1` across at least two distinct DBAPI connection lifecycles where practical
- create test-only parent/child tables with a real FK
- prove invalid child insert fails

Do not add production domain tables.

# H-008 — Documentation accuracy

After all corrections pass, update `docs/31_IMPLEMENTATION_PROGRESS.md` with a narrow subsection:

`Phase 1C.1 — Database foundation hardening`

Record:
- readiness 200/503 semantics
- SQL parameter privacy
- deterministic default DB location
- synchronous driver restriction
- FK readiness
- migration-head robustness
- strengthened architecture/FK tests

Do not mark overall Phase 1/v0.1.0 complete.
Do not rewrite frozen specs.

# Scope exclusions

Do NOT add:
- users/roles/permissions/role_permissions/user_sessions/user_preferences
- auth/RBAC/password hashing/session tokens/CSRF
- domain repositories
- jobs schema
- projects/datasets
- audit tables
- Admin routes
- ingestion/ML/LLM/simulation
- Redis/Celery
- async SQLAlchemy
- Streamlit
- React/Vue/Angular
- automatic migrations on startup
- production `Base.metadata.create_all()`

Do not begin Phase 1D.

No new dependency should be necessary. If you believe one is required, stop and report rather than adding it silently.

# Mandatory verification

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

Also run Alembic head/current checks against isolated test DBs and the existing upgrade/downgrade/re-upgrade migration tests.

If dependencies do not change, do not regenerate `requirements.lock`.

Verify:
- no local DB/runtime files tracked
- no Phase 1D functionality added
- no frontend framework/Streamlit changes

# Mandatory final response

Report:
1. starting SHA / branch / initial status
2. files created
3. files modified
4. exact correction for H-001 through H-008
5. test totals
6. Ruff/format/mypy/compile/pip results
7. readiness 200/503 evidence
8. SQL parameter leak-test evidence
9. deterministic default DB-path evidence
10. `sqlite+aiosqlite` rejection evidence
11. FK readiness and actual FK-violation evidence
12. migration multiple-head/safe-failure evidence
13. architecture/conformance scan results
14. generated/tracked DB artifact check
15. final git status and diff stat
16. unresolved issues

End exactly with one:

`Phase 1C.1: PASS — Phase 1D ready for independent review`

or

`Phase 1C.1: FAIL — Phase 1D blocked`

Do not begin Phase 1D.
