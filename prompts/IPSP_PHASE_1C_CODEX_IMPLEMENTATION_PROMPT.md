# IPSP v1.0 — Phase 1C Codex Implementation Prompt
## SQLite + SQLAlchemy 2.x + Alembic Control-Plane Foundation

You are implementing IPSP v1.0 in the existing repository.

**Authoritative repository:** `Kedar-Joshi07/IPSP`  
**Required starting point:** commit `0e4d35e9bc2ad6c3c6506f6aef6fdad4dd4754d9` or a direct descendant containing no unreviewed Phase 1C work.

Current gate state:
- Phase 0: COMPLETE
- Phase 0.5: PASS
- Documentation Freeze: PASS
- Phase 1A: PASS
- Phase 1A.1: PASS
- Phase 1B: FINAL PASS
- Phase 1C: AUTHORIZED
- Current application version remains `v0.1.0`

This task is **Phase 1C only**.

---

# 1. Governing rules

The frozen repository documentation is the implementation authority.

Do not redesign IPSP.

Phase 1C establishes the **SQLite control-plane persistence foundation**, not the application business schema.

Preserve all earlier gates, including:

- HTML/CSS/Vanilla JS frontend only;
- Python/FastAPI backend;
- no Streamlit;
- no runtime CDN dependencies;
- no benchmark/domain contamination;
- typed configuration as the sole process-config source;
- safe secret handling;
- backend outbound-policy enforcement;
- safe error envelopes;
- recursive log redaction;
- request/trace propagation;
- no JWT/python-jose browser-auth architecture;
- no actual outbound network implementation.

If a required database decision is not resolved by the frozen specifications and would materially constrain later architecture, stop and report it rather than silently inventing a new design.

---

# 2. Required reading before editing

Read completely before implementation:

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_PROJECT_STRUCTURE.md`
6. `docs/18_SECURITY_RBAC_SPEC.md`
7. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
8. `docs/23_ERROR_HANDLING_SPEC.md`
9. `docs/24_JOB_PROCESSING_SPEC.md`
10. `docs/27_SQLITE_SCHEMA_SPEC.md`
11. `docs/28_REST_API_CONTRACT.md`
12. `docs/29_TEST_STRATEGY.md`
13. `docs/30_ACCEPTANCE_CRITERIA.md`
14. `docs/31_IMPLEMENTATION_PROGRESS.md`
15. `docs/32_DECISION_LOG.md`
16. `docs/34_CODING_STANDARDS.md`
17. `docs/35_CONFIGURATION_SPEC.md`
18. `docs/37_SYSTEM_HEALTH_SPEC.md`
19. `docs/40_ANTI_CONTAMINATION.md`
20. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Then inspect the current Phase 1A–1B implementation, especially:

- `backend/ipsp/config/`
- `backend/ipsp/database/`
- `backend/ipsp/services/readiness.py`
- `backend/ipsp/api/routes/health.py`
- `backend/ipsp/main.py`
- `backend/ipsp/jobs/`
- `.env.example`
- `pyproject.toml`
- `requirements.lock`
- current tests

Before editing run:

```text
git status --short
git rev-parse HEAD
```

Preserve unrelated user-owned changes.

---

# 3. Frozen database rules that Phase 1C must enforce

The SQLite control plane is governed by these frozen rules:

- SQLite is the v1.0 control-plane database.
- SQLAlchemy is the ORM/data-access foundation.
- Use **synchronous SQLAlchemy 2.x** patterns.
- Use `select()`, `Session.execute()`, and `Session.scalars()`.
- `Session.query()` is prohibited.
- Do not hide synchronous SQLAlchemy work inside `async def`.
- Repositories mediate domain data access.
- Transactions wrap state transitions.
- Foreign keys are enabled.
- Migration history is mandatory.
- `database/migrations/` is the **single repository-wide Alembic history**.
- SQLAlchemy ORM entities are owned exactly once under `backend/ipsp/database/models/`.
- Pydantic API schemas remain separate from ORM models.
- No persisted `is_admin`.
- No persisted `is_multi_table`.
- Versioned/immutable business objects must later be represented through explicit version records rather than mutable counters/flags.

Phase 1C must build the infrastructure that makes those rules easy to follow later.

---

# 4. Phase 1C objective

Implement a production-quality database foundation containing:

1. typed database configuration;
2. canonical SQLAlchemy declarative base/metadata;
3. synchronous engine construction;
4. synchronous session factory/lifecycle;
5. transaction/session helper boundaries;
6. mandatory SQLite foreign-key enforcement;
7. Alembic configured at the single canonical migration root;
8. an initial **foundation/baseline migration** proving the migration pipeline;
9. migration-state inspection;
10. SQLite connectivity/readiness integration;
11. database composition in the existing application foundation;
12. database-focused tests;
13. updated dependency lock;
14. updated documentation/progress evidence.

This phase must **not** implement the business/security schema owned by later packages.

---

# 5. Explicitly DO NOT implement in Phase 1C

Do NOT create ORM tables for:

- users;
- roles;
- permissions;
- role_permissions;
- user_sessions;
- user_preferences;
- projects;
- datasets;
- dataset_versions;
- dataset_tables;
- dataset_columns;
- dataset permissions;
- semantic manifests;
- capabilities;
- models;
- simulations;
- LLM providers;
- audit events;
- jobs.

Those belong to their respective later implementation packages.

In particular:

- Phase 1D owns User/Role/Permission schema.
- Phase 1E owns authentication/session behavior.
- Phase 1F owns RBAC enforcement.
- Phase 1G owns durable audit/observability expansion.
- Phase 1H owns the SQLite-backed job repository/service/worker behavior.

Do not prematurely create “placeholder” business tables merely to make Alembic non-empty.

Do not implement:
- authentication;
- RBAC;
- password hashing;
- CSRF;
- API routes for database administration;
- dataset ingestion;
- ML;
- LLM providers;
- simulation;
- Redis/Celery;
- PostgreSQL support;
- async SQLAlchemy;
- `aiosqlite`;
- raw `sqlite3` application repositories;
- automatic schema creation using `Base.metadata.create_all()`.

---

# 6. Dependencies

Add maintained compatible direct dependencies for:

- SQLAlchemy 2.x
- Alembic

Resolve maintained compatible versions at implementation time from authoritative package sources.

Requirements:

- add them to `pyproject.toml`;
- refresh `requirements.lock` reproducibly;
- do not add `sqlite3` as a pip dependency;
- do not add `aiosqlite`;
- do not add an async SQLAlchemy stack;
- do not add PostgreSQL drivers;
- explain every direct dependency change.

After dependency changes, repeat a clean-environment lock verification using the repository's canonical Phase 1 Python runtime.

The prior lock snapshot was verified on Python 3.12. Do not claim cross-Python portability unless separately tested.

---

# 7. Typed database configuration

Extend the existing typed `Settings` tree with a cohesive database configuration model.

Prefer a nested shape such as:

```text
IPSP_DATABASE__URL=...
IPSP_DATABASE__ECHO=false
```

Exact fields should remain minimal.

At minimum support:

- database URL/location;
- SQL echo/logging switch if useful for development;
- an explicit SQLite connection timeout if implemented.

Rules:

- default must be local SQLite;
- configuration must remain non-secret;
- do not scatter `os.getenv()` calls;
- environment names must be documented in `.env.example`;
- paths/URLs must not be duplicated as independent sources of truth;
- invalid or unsupported database configuration must fail safely;
- if a non-SQLite URL is supplied in v1.0, fail with a clear validated unsupported-backend error rather than accidentally attempting an unfrozen backend.

Do not put credentials into the default database URL.

---

# 8. Canonical SQLAlchemy base and metadata

Create the sole declarative base under:

```text
backend/ipsp/database/models/
```

A likely structure is:

```text
backend/ipsp/database/models/base.py
```

Requirements:

- use SQLAlchemy 2.x `DeclarativeBase`;
- use typed ORM conventions compatible with future `Mapped[...]` / `mapped_column(...)`;
- keep one canonical `MetaData`;
- use deterministic constraint/index naming if appropriate for reliable Alembic migrations;
- no duplicate `Base` elsewhere;
- no business entity tables in Phase 1C.

If you introduce a reusable persistence helper such as a UTC-aware datetime type, it must:
- have tests;
- preserve timezone-aware UTC semantics through SQLite round-trips;
- not create a second timestamp convention;
- be documented as foundation infrastructure.

If this cannot be done cleanly without an architectural decision, defer it and report the limitation rather than adding an ad-hoc timestamp convention.

---

# 9. Engine construction

Implement an explicit synchronous engine factory.

The engine must:

- use SQLAlchemy 2.x;
- support the configured local SQLite database;
- enforce SQLite foreign keys on **every connection**;
- use safe FastAPI-compatible SQLite connection settings where needed;
- avoid global mutable engine creation at import time;
- not create schema automatically;
- not run migrations automatically;
- not perform hidden network behavior;
- remain injectable/testable.

SQLite-specific connection setup must be centralized.

At minimum verify:

```sql
PRAGMA foreign_keys
```

returns enabled on connections created by the production engine factory.

Do not enable additional SQLite modes such as WAL merely as an unreviewed optimization. If you believe WAL or another persistent PRAGMA is required, treat it as an architectural decision and report it rather than silently adding it.

---

# 10. Session lifecycle and transaction foundation

Implement a synchronous session factory and clear lifecycle boundary.

A reasonable design may include:

- `sessionmaker`;
- a `DatabaseSessionFactory`/equivalent;
- a context manager for short-lived sessions;
- an explicit transaction helper.

Required behavior:

- sessions are not global singletons;
- commit occurs only when the caller explicitly uses the transaction boundary;
- exceptions roll back the active transaction;
- sessions are closed reliably;
- nested hidden commits are avoided;
- repositories later receive/inherit an explicit session boundary;
- no business repository is needed yet.

Do not put database access in FastAPI routes in this phase.

Do not write synchronous Session code in `async def`.

---

# 11. Alembic: one canonical migration history

Replace the existing migration placeholder with a real Alembic environment rooted only at:

```text
database/migrations/
```

Expected components may include:

```text
alembic.ini
database/migrations/env.py
database/migrations/script.py.mako
database/migrations/versions/
```

The exact config layout may differ, but there must be exactly one Alembic history.

Requirements:

- Alembic obtains the database URL from the canonical IPSP configuration;
- metadata points to the canonical SQLAlchemy Base;
- no hardcoded second SQLite path;
- offline and online migration modes work;
- migration commands work from the repository root;
- no package-local migrations directory is introduced;
- no import-time migration execution;
- no automatic application-startup `upgrade head`.

Create one initial **empty foundation/baseline revision** whose purpose is to prove the migration pipeline.

The baseline revision must not create Phase 1D+ business tables.

Verify:

- upgrade from empty DB to `head`;
- current revision equals head;
- downgrade to `base`;
- upgrade back to head.

A freshly upgraded database should contain Alembic's version bookkeeping but no IPSP business tables yet.

---

# 12. Migration-state service

Implement a small database/migration inspection boundary suitable for readiness.

It should be able to determine, without mutating schema:

- current database revision;
- expected Alembic head revision;
- whether the database is at head.

Requirements:

- inspection is side-effect free;
- it does not auto-upgrade;
- it returns safe structured information;
- raw filesystem/config details should not leak to unauthenticated callers.

Keep it independent of FastAPI.

---

# 13. Database readiness integration

The frozen health specification says readiness must eventually consider required SQLite and migration state.

After Phase 1C, SQLite becomes an active dependency, so update readiness accordingly.

`/health/live` remains unchanged and minimal.

`/health/ready` should minimally evaluate:

- application/configuration readiness;
- SQLite connection success;
- migration state at expected head.

Rules:

- no schema mutation during readiness;
- no auto-migration;
- no raw DB URL/path/exception traceback in the response;
- use explicit exception handling;
- a missing/unavailable DB or migration mismatch produces a minimal not-ready result with a stable safe code/status;
- a denied outbound policy is not a readiness failure;
- future dependencies such as analytical storage/job worker may remain deferred until their implementation packages.

Decide the HTTP status consistently with the existing health contract/spec. If the frozen docs do not specify a changed HTTP status, preserve current external behavior and expose a safe readiness status rather than inventing a breaking API contract.

Add tests.

---

# 14. Application composition

Extend existing explicit foundation composition.

The application should be able to obtain:

- Settings;
- feature flags;
- SecretProvider;
- OutboundPolicy;
- database engine/session services;
- migration-state/readiness dependency.

Avoid:

- mutable global engines;
- module import side effects;
- generic service-locator calls scattered through domain code.

The DB foundation must remain independently unit-testable outside FastAPI.

---

# 15. Error handling

Reuse current `IPSPError` infrastructure.

Introduce only the minimum database-specific safe error codes/classes needed, consistent with the frozen taxonomy.

Examples of concerns:

- unsupported database backend;
- database unavailable;
- database not at required migration revision.

Do not expose:

- database URLs containing credentials;
- filesystem paths unnecessarily;
- SQL statements with sensitive values;
- raw SQLAlchemy tracebacks;
- raw exception strings in API responses.

Internal logging must remain sanitized.

---

# 16. SQLite test isolation

Database tests must never use the developer's real `ipsp.db`.

Use temporary directories/files or an explicitly test-scoped in-memory database.

If using `sqlite:///:memory:` in tests, account correctly for SQLite connection scope/pooling so separate Sessions do not accidentally point to separate unrelated in-memory databases.

The production factory must not be distorted merely to satisfy tests.

---

# 17. Required database tests

Add meaningful tests at minimum for:

## Configuration
- default backend is SQLite;
- nested database environment variables load correctly;
- malformed/unsupported backend is rejected safely;
- safe settings snapshot contains no database secret.

## Engine
- engine is SQLAlchemy 2.x synchronous engine;
- SQLite foreign keys are enabled;
- no schema is created merely by creating the engine;
- test DB path is isolated;
- no engine is constructed at import time if the architecture allows verification.

## Session/transactions
- session opens/closes correctly;
- explicit transaction commits;
- exception rolls back;
- a failed transaction does not leave partial state;
- session helpers are synchronous.

Because Phase 1C cannot create business ORM tables, use a test-only temporary SQLAlchemy table/model or SQL text fixture under tests to prove transaction semantics. Do not add a production placeholder table.

## Alembic
- exactly one migration root exists;
- empty DB can upgrade to head;
- current revision equals head after upgrade;
- downgrade to base works;
- upgrade back to head works;
- baseline migration creates no IPSP business tables;
- Alembic URL comes from canonical settings/config rather than a duplicate hardcoded path.

## Readiness
- healthy migrated DB reports ready;
- unavailable DB reports not ready safely;
- DB behind migration head reports not ready;
- readiness does not mutate schema or auto-upgrade;
- liveness remains independent of DB state.

## Architecture
- no `Session.query()`;
- no async SQLAlchemy;
- no `aiosqlite`;
- no `Base.metadata.create_all()` in production source;
- one canonical Declarative Base;
- one canonical Alembic root;
- no Phase 1D+ business ORM tables;
- no Streamlit;
- no benchmark contamination;
- no runtime CDN;
- no actual external network implementation.

---

# 18. Migration command documentation

Document the canonical developer commands, e.g.:

```text
alembic upgrade head
alembic current
alembic downgrade base
```

Commands must work from repository root using the committed Alembic config.

Document that:

- developers run migrations explicitly;
- application startup does not auto-upgrade;
- production deployment must migrate before readiness passes;
- `Base.metadata.create_all()` is not the deployment mechanism.

Do not add shell-specific commands as the only supported workflow.

---

# 19. Dependency/clean-environment verification

Because SQLAlchemy and Alembic are new direct dependencies:

1. create a fresh temporary virtual environment using the canonical Phase 1 Python runtime;
2. install `requirements.lock`;
3. install local IPSP package with `--no-deps`;
4. run `pip check`;
5. run the full test suite;
6. run Ruff lint;
7. run Ruff format check;
8. run strict mypy;
9. run compileall;
10. execute the Alembic upgrade/current/downgrade/upgrade cycle against a temporary DB.

Remove the temporary environment/database afterward.

Report the Python version used.

Do not claim exact lock portability across Python versions not tested.

---

# 20. Documentation updates

After all gates pass, update:

- `.env.example`
- `README.md` if needed
- `config/README.md`
- `database/migrations/README.md` or replace it with accurate Alembic usage documentation
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Record:

`Phase 1C — SQLite + SQLAlchemy 2.x + Alembic Control-Plane Foundation`

Do not mark the full Phase 1/v0.1.0 milestone complete.

Update `docs/32_DECISION_LOG.md` only if a genuine architecture decision was required.

Do not rewrite frozen specs to make implementation drift appear compliant.

---

# 21. Git discipline

Before editing:

```text
git status --short
git rev-parse HEAD
```

After implementation:

```text
git status --short
git diff --stat
git diff --check
```

Do not automatically commit or push unless explicitly requested by the user.

Do not add:

- real SQLite runtime databases;
- temporary migration DBs;
- `.env`;
- virtual environments;
- caches;
- logs;
- ZIP archives;
- secrets.

Ensure relevant local DB patterns are ignored without accidentally ignoring legitimate SQL/migration source files.

---

# 22. Phase 1C acceptance gate

Phase 1C is PASS only if all are true:

- SQLAlchemy 2.x synchronous foundation exists;
- Alembic foundation exists;
- exactly one canonical Declarative Base exists;
- exactly one canonical migration history exists;
- database config is typed and canonical;
- SQLite foreign keys are enabled on every connection;
- no business/security tables from Phase 1D+ were introduced;
- no `create_all()` production migration shortcut exists;
- no automatic startup migration exists;
- no async SQLAlchemy/aiosqlite exists;
- session lifecycle is explicit and transaction rollback is proven;
- Alembic baseline can upgrade/downgrade/upgrade cleanly;
- migration state can be inspected without mutation;
- readiness now reflects SQLite connectivity and migration currency safely;
- liveness remains independent/minimal;
- no DB URLs/secrets/raw errors leak;
- new dependencies are locked reproducibly;
- full prior test suite still passes;
- Ruff/mypy/compile/pip checks pass;
- anti-contamination/Streamlit/CDN/network scans pass;
- progress documentation is accurate.

---

# 23. Mandatory final response

Return all sections below.

## A. Starting state
- starting SHA;
- branch;
- initial `git status --short`.

## B. Files created
List every created file.

## C. Files modified
List every modified file.

## D. Database architecture
Explain:
- database settings;
- canonical Base/metadata;
- engine creation;
- SQLite connection handling;
- session/transaction lifecycle;
- composition wiring.

## E. Alembic architecture
Explain:
- migration root;
- configuration source;
- baseline revision;
- upgrade/downgrade behavior;
- migration-state inspection.

## F. Readiness integration
Explain:
- SQLite connectivity check;
- migration-head check;
- failure behavior;
- deferred dependencies.

## G. Dependencies
List added/changed direct dependencies and resolved versions.
Explain why each is required.

## H. Tests
Give exact:
- passed;
- failed;
- skipped;
- warnings.

## I. Database/migration verification
Report:
- foreign-key PRAGMA result;
- fresh DB upgrade;
- `current`;
- downgrade to base;
- re-upgrade to head;
- business-table scan;
- no auto-migration/create-all evidence.

## J. Quality gates
Report:
- compileall;
- Ruff lint;
- Ruff format;
- strict mypy;
- pip check;
- git diff check.

## K. Clean-environment verification
Report:
- Python version;
- lock install;
- local package install;
- tests;
- quality gates;
- Alembic cycle.

## L. Architecture/conformance
Explicitly report:
- canonical ORM ownership;
- number/location of Alembic roots;
- `Session.query()` scan;
- async SQLAlchemy/aiosqlite scan;
- production `create_all()` scan;
- premature Phase 1D+ ORM tables;
- benchmark/business contamination;
- Streamlit;
- runtime CDN;
- JWT/python-jose;
- actual outbound/network calls.

## M. Git state
Show:
- final `git status --short`;
- `git diff --stat`.

## N. Deviations / unresolved issues
If none, say `None`.

## O. Gate result

End exactly with one of:

`Phase 1C: PASS — ready for independent review before Phase 1D`

or

`Phase 1C: FAIL — Phase 1D blocked`

Do not begin Phase 1D.
