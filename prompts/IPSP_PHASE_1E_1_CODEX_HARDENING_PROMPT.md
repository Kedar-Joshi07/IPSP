# IPSP v1.0 — Phase 1E.1 Codex Security Hardening Prompt
## Authentication Failure Timing + CSRF/Fixation Regression Coverage

Repository: `Kedar-Joshi07/IPSP`
Required starting point: `d91c40b8083b9c719edf07a1c5fb39aa56ba7b91`

Phase 1E is structurally strong, but independent review found one authentication side-channel hardening issue plus two explicit regression-coverage gaps. Phase 1F remains blocked until this narrow pass is complete.

Do not redesign authentication. Do not add dependencies. Do not begin RBAC.

# 1. Read before editing

Read:
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `backend/ipsp/auth/passwords.py`
- `backend/ipsp/auth/service.py`
- `backend/ipsp/api/dependencies/auth.py`
- `tests/unit/test_auth.py`
- `tests/integration/test_auth_api.py`
- `tests/architecture/test_conformance.py`

Run:
```text
git status --short
git rev-parse HEAD
```

Preserve user-owned prompt files.

# H-001 — Equalize Argon2 cost for disabled and locked failures

Current behavior:
- unknown username -> dummy Argon2 verification
- active user + wrong password -> real Argon2 verification
- disabled user -> no Argon2 verification
- currently locked user -> no Argon2 verification

Although all cases return the same 401 body, disabled/locked accounts currently have a much cheaper failure path. Fix this timing/state side channel.

Required:
```text
unknown user       -> 1 dummy Argon2 verification
disabled user      -> 1 dummy Argon2 verification
currently locked   -> 1 dummy Argon2 verification
active wrong pass  -> 1 real Argon2 verification
active correct     -> 1 real Argon2 verification
```

Do not do both real and dummy verification for normal wrong-password attempts. Do not verify the disabled/locked user's real stored hash just for timing; use the dummy path.

Prefer replacing the hard-coded dummy Argon2 hash with one generated once when `PasswordService` is constructed using the same active `PasswordHash.recommended()` policy. Do not generate it per request. The dummy credential is non-secret and can never authenticate.

Tests must use deterministic spies/mocks, not flaky wall-clock assertions. Prove:
- unknown user invokes dummy verification exactly once
- disabled user invokes it exactly once
- locked user invokes it exactly once
- ordinary wrong password does not invoke an additional dummy verification
- successful login does not invoke dummy verification

All failure cases must retain identical generic 401 code/message.

# H-002 — Complete CSRF isolation regressions

Add integration tests for the two missing explicit cases:

1. Valid authenticated session + CSRF header present + CSRF cookie missing -> HTTP 403 `AUTHZ-CSRF_INVALID`.
2. CSRF token from another valid session cannot authorize the current session.

Cross-session test:
```text
session A bearer cookie + session B CSRF cookie/header
    -> 403 AUTHZ-CSRF_INVALID
```

Retain existing coverage for missing header, mismatch, persisted hash mismatch, Unicode input, and no raw-token logging.

Production CSRF redesign should not be needed unless a regression exposes a real defect.

# H-003 — Explicit attacker-chosen session fixation regression

Add a test that:
1. places `ATTACKER_CHOSEN_SESSION_DO_NOT_ACCEPT` in the configured session cookie before login
2. performs valid login
3. proves returned session cookie is different and server-generated
4. proves the attacker-selected raw cookie value is not persisted
5. proves the attacker-selected hash is not the newly authenticated session
6. proves the stored token hash matches only the new issued bearer token

Do not print/log the marker.

No production change should be needed unless the test fails.

# Scope lock

Do NOT add/change:
- RBACService / permission enforcement
- permission decorators/dependencies
- user/role/permission management API
- dataset ACL
- JWT/python-jose/PyJWT
- bcrypt/passlib
- Redis/Celery
- async SQLAlchemy
- auth cookie architecture
- token hashing algorithm
- CSRF architecture
- session TTL/lockout defaults
- frontend/UI
- Streamlit/React/Vue/Angular
- runtime network calls
- `pyproject.toml`
- `requirements.lock`
- ORM tables or migrations

No dependency change is expected. Do not regenerate the lock or create clean dependency-resolution virtual environments.

# Documentation

Update `docs/31_IMPLEMENTATION_PROGRESS.md` with a narrow subsection:
`Phase 1E.1 — Authentication side-channel and regression hardening`

Record:
- disabled/locked dummy Argon2 equalization
- dummy hash aligned to active Argon2 policy
- missing-cookie/cross-session CSRF regressions
- attacker-selected fixation regression
- test/quality evidence

Do not mark Phase 1 complete. Do not begin Phase 1F.

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

Confirm:
- `pyproject.toml` unchanged
- `requirements.lock` unchanged
- no new migration/table
- five-table ORM allowlist unchanged
- no raw password/session/CSRF/fixation marker appears in logs
- no Phase 1F code appears

# Mandatory final report

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. H-001
Exact failure-cost behavior and dummy-hash construction.

## E. H-002
Missing-cookie and cross-session CSRF evidence.

## F. H-003
Attacker-selected session-fixation evidence.

## G. Public error equivalence
Confirm unknown, wrong-password, disabled and locked login remain identical safe 401 responses.

## H. Leak evidence
Passwords, raw bearer tokens, raw CSRF values and fixation marker absent from logs/responses/persistence.

## I. Tests
Exact passed/failed/skipped/warnings.

## J. Quality gates
Compileall, Ruff lint/format, mypy, pip check, diff check.

## K. Dependency/schema state
Confirm pyproject/lock unchanged, no new dependency/migration/table.

## L. Phase-boundary conformance
Confirm no RBAC, JWT, bcrypt/passlib, async SQLAlchemy, Streamlit/framework/network drift.

## M. Git state
Final status and diff stat.

## N. Unresolved issues
If none: `None`

## O. Gate result

End exactly with one:
`Phase 1E.1: PASS — Phase 1F ready for independent review`
or
`Phase 1E.1: FAIL — Phase 1F blocked`

Do not begin Phase 1F.
