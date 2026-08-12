# IPSP v1.0 — Phase 1G.1 Codex Observability Hardening Prompt
## Authenticated Context Propagation + Multi-Sink Correlation + Static-Message Guard

Repository: `Kedar-Joshi07/IPSP`
Required starting point: `42bbdb1b7812bccc01143c5c1f5ae74fdda5041f`

Phase 1G is structurally strong, but independent review found one important authenticated-context propagation defect and two observability regression gaps. Phase 1H remains blocked until this narrow pass is complete.

Do not redesign audit/RBAC/auth. Do not add dependencies or migrations. Do not begin Phase 1H.

# Read first
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `backend/ipsp/observability/context.py`
- `backend/ipsp/observability/events.py`
- `backend/ipsp/observability/logging.py`
- `backend/ipsp/errors/handlers.py`
- `backend/ipsp/api/dependencies/auth.py`
- `backend/ipsp/api/dependencies/rbac.py`
- `backend/ipsp/api/routes/auth.py`
- `tests/unit/test_logging.py`
- `tests/integration/test_app.py`
- `tests/integration/test_observability.py`
- `tests/integration/test_auth_api.py`
- `tests/architecture/test_conformance.py`

Run:
```text
git status --short
git rev-parse HEAD
```

# H-001 — Bind authenticated ContextVars in the request task, not only a sync worker

Current `require_authenticated_session()` is synchronous and calls `bind_authenticated_context()` inside that synchronous dependency. FastAPI executes sync dependencies/endpoints in worker threads; AnyIO copies context into a worker but changes made in the worker do not propagate back to the calling async task.

`request.state` is therefore reliable for request-completion logging and current audit producers that pass identity explicitly remain correct, but the generic ContextVar contract is incomplete: separately executed downstream dependencies/routes/loggers cannot reliably inherit `user_id`, `session_correlation_id`, and `resolved_role`.

Required correction:

Use a two-stage dependency boundary:

```text
sync authentication helper
    -> runs AuthService.authenticate_session / DB work

async require_authenticated_session wrapper
    -> receives AuthPrincipal
    -> writes request.state
    -> calls bind_authenticated_context in request/event-loop task
    -> returns principal
```

Do NOT run synchronous SQLAlchemy directly inside async code. Keep AuthService/repositories synchronous. Do not add AsyncSession/aiosqlite/async engine.

Preserve:
- dependency caching
- 401/403 semantics
- CSRF
- request.state fields
- role identity as context only
- no bearer/CSRF/cookie values in observability context

Required tests:
1. protected sync route calling `current_observability_context()` sees user_id/session correlation/resolved role/trace/request IDs;
2. downstream sync dependency after authentication sees same identity;
3. authenticated handled error/runtime JSONL event includes identity context without logger manually receiving identity;
4. anonymous request after authenticated request does not inherit identity;
5. two users in concurrent/interleaved requests cannot cross-contaminate identity context;
6. existing request.state tests remain green.

No timing-based tests.

# H-002 — Freeze generated trace/request IDs on the LogRecord

`JsonFormatter` already freezes generated event_id and timestamp on a LogRecord. But for a non-request record without explicit trace/request IDs, each handler invocation can generate different trace/request IDs. The same event may therefore have identical event_id but different correlation IDs in console vs JSONL.

Required:
For one LogRecord, all IPSP-managed handlers must share exactly:
- timestamp_utc
- event_id
- trace_id
- request_id

When no active IDs exist, resolve/generate them once and store them on the LogRecord so later handlers reuse them.

Do not derive these IDs from event_id, bearer token, token hash, or session correlation ID.

Tests:
- format same LogRecord twice outside request context and assert all four identities match;
- exercise real console + JSONL two-handler path where practical and assert identical event/trace/request/timestamp.

# H-003 — Enforce developer-controlled static log messages

`record.getMessage()` is intentionally not redacted, so production logger message strings must stay static and all runtime/user values must use sanitized structured metadata.

Add a narrow AST architecture test over `backend/ipsp/**/*.py` for:
- logger.debug
- logger.info
- logger.warning
- logger.error
- logger.exception
- logger.critical

Require:
- first positional message arg is a literal string constant;
- no extra positional formatting args;
- runtime data goes through `extra` / `ipsp_metadata` / typed fields.

Do not scan tests, migrations, third-party code, or print statements.

Correct any existing production logger call that violates this without weakening the rule.

# Scope lock

Do NOT change:
- audit_events schema
- migration `20260812_04`
- six-table ORM allowlist
- event stream catalog
- audit action names
- audit durability policy
- RBAC authority/catalog
- login timing/lockout/session/CSRF/cookies
- JSONL rotation defaults
- pyproject
- requirements.lock
- frontend
- jobs/Admin health/Phase 1H

No dependency or migration change is expected.

# Documentation

Update `docs/31_IMPLEMENTATION_PROGRESS.md` with:
`Phase 1G.1 — Observability context and correlation hardening`

Record H-001/H-002/H-003 and exact quality evidence. Do not mark Phase 1 complete.

# Verify

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
- head still `20260812_04`
- six-table allowlist unchanged
- pyproject/lock unchanged
- no Phase 1H code

# Final report

## A. Starting state
## B. Files created
## C. Files modified
## D. H-001 authenticated context propagation
## E. H-002 multi-sink correlation
## F. H-003 static-message guard
## G. Authentication/RBAC regression
## H. Observability regression
## I. Tests
## J. Quality gates
## K. Dependency/schema state
## L. Phase boundary
## M. Git state
## N. Unresolved issues
## O. Gate result

End exactly with:
`Phase 1G.1: PASS — Phase 1H ready for independent review`
or
`Phase 1G.1: FAIL — Phase 1H blocked`

Do not begin Phase 1H.
