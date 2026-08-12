# IPSP v1.0 — Phase 1F.1 Codex Hardening Prompt
## Safe RBAC Synchronization CLI Failure Boundary

Repository: `Kedar-Joshi07/IPSP`
Required starting point: `8adfe94b021e5fe26b7a5b3d81f66a545dfcc8a5`

Phase 1F is structurally correct, but independent review found one narrow acceptance/security defect in the new `ipsp-sync-rbac` CLI. Phase 1G remains blocked until this correction is reviewed.

Do not redesign RBAC. Do not add dependencies or migrations. Do not begin Phase 1G.

# Read first
- `backend/ipsp/cli/rbac.py`
- `backend/ipsp/database/migrations.py`
- `backend/ipsp/config/settings.py`
- `backend/ipsp/config/providers.py`
- `backend/ipsp/auth/rbac.py`
- `tests/integration/test_rbac.py`
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Run:
```text
git status --short
git rev-parse HEAD
```

# H-001 — Safe CLI failure boundary

Current `ipsp-sync-rbac` catches only `IPSPError`. `MigrationStateService.inspect()` can raise `MigrationStateError`; database inspection can raise SQLAlchemy errors; Settings construction can raise Pydantic validation errors. Those expected operational failures can currently escape as a traceback, exposing local paths/internal implementation details and violating the Phase 1F requirement that the CLI fail safely.

Required behavior:
1. success returns 0;
2. expected configuration/database/migration/RBAC failures return non-zero;
3. user-visible failure is generic and safe;
4. never print raw exception text, SQL, DB URLs, filesystem paths, passwords, tokens, CSRF values, or stack traces;
5. dispose the engine whenever services were successfully constructed;
6. preserve ordinary stale-database handling;
7. do not swallow `KeyboardInterrupt` or `SystemExit`.

Use a finite expected-exception boundary. It is acceptable to translate `MigrationStateError` / SQLAlchemy inspection failures into safe `IPSPError`, or catch expected operational types in the CLI and print a generic safe message. Do not add audit/logging infrastructure.

# Tests

Add focused tests proving:
- stale/below-head DB refusal remains safe;
- mocked `MigrationStateError` makes CLI return non-zero without traceback/internal detail;
- mocked SQLAlchemy/database inspection error returns non-zero without raw error/DB path;
- invalid Settings/config input returns non-zero without echoing the raw invalid value;
- success and idempotent no-op behavior remain unchanged;
- password/session/CSRF/token markers are not printed;
- engine disposal occurs on failure after services construction.

# Scope lock

Do not change RBAC authority, permission catalog, provisioning policy, `has_permission`, `enforce_permission`, privilege invalidation, bootstrap behavior, ORM schema, migrations, authentication/session/CSRF behavior, frontend, `pyproject.toml`, or `requirements.lock`.

# Documentation

Add a narrow `Phase 1F.1 — RBAC CLI safe-failure hardening` subsection to `docs/31_IMPLEMENTATION_PROGRESS.md`. Record safe operational failure handling and regression evidence. Do not mark Phase 1 complete.

# Quality gates

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

Confirm:
- `pyproject.toml` unchanged
- `requirements.lock` unchanged
- Alembic head still `20260811_03`
- five-table ORM allowlist unchanged
- no Phase 1G code

# Final report

## A. Starting state
## B. Files created
## C. Files modified
## D. Failure-boundary correction
## E. Privacy evidence
## F. CLI behavior
## G. Resource cleanup
## H. Tests
## I. Quality gates
## J. Dependency/schema state
## K. Phase boundary
## L. Git state
## M. Unresolved issues
## N. Gate result

End exactly with:
`Phase 1F.1: PASS — Phase 1G ready for independent review`
or
`Phase 1F.1: FAIL — Phase 1G blocked`

Do not begin Phase 1G.
