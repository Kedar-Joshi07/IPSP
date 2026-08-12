# IPSP v1.0 — Phase 1E Codex Implementation Prompt
## Authentication, Argon2id Passwords, Server-Side Sessions, CSRF, Lockout & Bootstrap Admin

You are implementing the next reviewed work package in the existing IPSP repository.

**Repository:** `Kedar-Joshi07/IPSP`
**Required starting point:** commit `7b8a6bd0c6224bc14c070c1e403b6739a81e2fb2` or an exact direct descendant containing no unreviewed Phase 1E work.

Current reviewed gate state:
- Phase 0: COMPLETE
- Phase 0.5: PASS
- Documentation Freeze: PASS
- Phase 1A: PASS
- Phase 1A.1: PASS
- Phase 1B: FINAL PASS
- Phase 1C: FINAL PASS
- Phase 1C.1: FINAL PASS
- Phase 1D: FINAL PASS
- Phase 1E: AUTHORIZED
- Application version remains `v0.1.0`

This task is **Phase 1E only**.

Do **not** begin Phase 1F RBAC permission enforcement.

# 1. Frozen security authorities

The frozen repository documentation is the authority.

Phase 1E implements authentication and session security while preserving:

```text
User.role_id
    ↓
Role
    ↓
RolePermission
    ↓
Permission
```

Phase 1E may resolve a user's role identity for session/user context, but it must not enforce application permissions.

Frozen rules:
1. Passwords use maintained `pwdlib[argon2]`.
2. New password hashes are Argon2id.
3. No bcrypt fallback unless explicit legacy migration is later approved.
4. Plaintext passwords are never stored.
5. Browser login uses opaque server-side sessions, not JWT.
6. Every successful login issues a new cryptographically random session token.
7. Only a cryptographic hash of the raw session token is persisted.
8. Raw session tokens are never logged.
9. Sessions have explicit expiry.
10. Logout invalidates the server-side session.
11. Password changes invalidate all sessions for that user.
12. Role/privilege changes must be able to invalidate sessions; Phase 1F will call that primitive.
13. Disabled users cannot authenticate or continue with an old session.
14. Failed authentication is throttled/account-locked temporarily.
15. Cookies are HttpOnly and Secure under HTTPS/production.
16. Localhost/development insecure-cookie behavior is explicit and cannot weaken production defaults.
17. State-changing authenticated browser requests enforce CSRF.
18. Session timestamps are timezone-aware UTC.
19. `session_correlation_id` is non-secret and never the bearer token/cookie.
20. No persisted `is_admin`.
21. No JWT/python-jose.
22. No localStorage authentication-token design.
23. Phase 1C.1 SQL parameter hiding remains enabled.

# 2. Read before editing

Read:
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/00_SCOPE_FREEZE.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `docs/40_ANTI_CONTAMINATION.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Inspect:
- `backend/ipsp/database/models/security.py`
- `backend/ipsp/database/types.py`
- `backend/ipsp/database/session.py`
- `backend/ipsp/database/engine.py`
- `backend/ipsp/config/settings.py`
- `backend/ipsp/config/providers.py`
- `backend/ipsp/security/redaction.py`
- `backend/ipsp/errors/exceptions.py`
- `backend/ipsp/errors/handlers.py`
- `backend/ipsp/observability/context.py`
- `backend/ipsp/observability/logging.py`
- `backend/ipsp/api/router.py`
- `backend/ipsp/api/routes/`
- `backend/ipsp/api/schemas/`
- `database/migrations/versions/20260811_02_phase1d_security_schema.py`
- current tests
- `pyproject.toml`
- `requirements.lock`

Before editing:

```text
git status --short
git rev-parse HEAD
```

Preserve unrelated user-owned/untracked prompt files.

# 3. Phase 1E objective

Implement:
1. Argon2id password hashing/verification;
2. typed auth/session settings;
3. concrete synchronous auth repositories;
4. `user_sessions` ORM table;
5. Alembic migration;
6. opaque session token issuance;
7. SHA-256 token-hash persistence;
8. session rotation/fixation protection;
9. explicit expiry;
10. logout invalidation;
11. all-session invalidation after password change;
12. disabled-user enforcement;
13. account lockout;
14. CSRF token generation/hash validation;
15. secure cookie helpers;
16. `/api/v1/auth/login`;
17. `/api/v1/auth/logout`;
18. `/api/v1/auth/me`;
19. `/api/v1/auth/change-password`;
20. reusable auth/CSRF dependencies;
21. first-admin CLI;
22. tests;
23. dependency lock refresh + clean environment verification.

No permission enforcement.

# 4. Out of scope

Do NOT implement:
- RBACService / has_permission / enforce_permission
- permission dependencies
- user/role/permission management API
- role changes through API
- role-to-permission production seeding
- dataset ACL
- Admin UI
- frontend login UI
- audit_events persistence
- user_preferences
- refresh tokens
- JWT
- OAuth/OIDC/SAML/MFA
- password reset email flows
- API keys
- remember-me
- Redis/Celery
- async SQLAlchemy
- remote auth providers
- outbound network calls
- Streamlit
- React/Vue/Angular

# 5. Dependency policy

Add maintained `pwdlib[argon2]`.

Requirements:
- resolve current maintained compatible version using official APIs/docs;
- Argon2id new hashes;
- no bcrypt/passlib/python-jose/PyJWT;
- no cryptography just for auth;
- no session package;
- stdlib `secrets`, `hashlib`, `hmac`, `uuid`, `getpass` are sufficient otherwise.

Update `pyproject.toml` and `requirements.lock`.

Because dependencies change:
- create disposable clean Python 3.12 environment(s);
- regenerate exact lock reproducibly;
- independently verify exact lock in a fresh environment where practical;
- install local IPSP `--no-deps`;
- run pip check/tests/Ruff/mypy/compileall;
- remove disposable clean envs afterward.

Report new transitive dependencies.

# 6. Auth configuration

Add immutable nested auth settings under canonical Settings, preferably:

```text
IPSP_AUTH__SESSION_TTL_MINUTES
IPSP_AUTH__FAILED_LOGIN_THRESHOLD
IPSP_AUTH__LOCKOUT_MINUTES
IPSP_AUTH__SESSION_COOKIE_NAME
IPSP_AUTH__CSRF_COOKIE_NAME
IPSP_AUTH__CSRF_HEADER_NAME
IPSP_AUTH__COOKIE_SECURE
IPSP_AUTH__COOKIE_SAMESITE
```

Recommended defaults unless frozen docs conflict:

```text
session_ttl_minutes = 480
failed_login_threshold = 5
lockout_minutes = 15
session_cookie_name = ipsp_session
csrf_cookie_name = ipsp_csrf
csrf_header_name = X-CSRF-Token
cookie_secure = true
cookie_samesite = lax
```

Requirements:
- typed/validated;
- TTL > 0;
- threshold >= 1;
- lockout > 0;
- safe cookie/header names;
- SameSite only `lax` or `strict`;
- production fails closed if `cookie_secure=false`;
- development may explicitly set false for localhost HTTP;
- no secret values in Settings;
- no app-wide randomly generated auth secret is required.

Do not add a password pepper unless frozen docs require one.

# 7. Password service

Create under `backend/ipsp/auth/`.

Implement:
- Argon2id hash;
- verify;
- detect/update rehash when supported by pwdlib;
- no plaintext/hash logging;
- no bcrypt legacy fallback.

Unknown-user timing equalization:
- unknown username still performs one Argon2 verification against a valid non-secret dummy Argon2id hash;
- dummy hash can never authenticate;
- external response remains generic.

Do not reveal whether username exists, password is wrong, account is disabled, or account is locked.

# 8. Password input boundary

At minimum:
- reject empty password;
- cap unreasonable oversized input to reduce hashing DoS;
- do not trim;
- preserve Unicode;
- never log validation values.

Do not invent a broad complexity/history policy.

# 9. user_sessions ORM table

Phase 1E adds exactly one new production ORM table:

```text
user_sessions
```

Expected ORM table allowlist:

```text
permissions
role_permissions
roles
user_sessions
users
```

Canonical ORM ownership remains only in `backend/ipsp/database/models/`.

# 10. user_sessions schema

Required fields:

```text
id
token_hash
csrf_token_hash
session_correlation_id
user_id
created_at
last_seen_at
expires_at
invalidated_at
```

Requirements:
- integer PK;
- token_hash non-null unique;
- csrf_token_hash non-null;
- session_correlation_id non-null unique;
- user_id non-null FK users.id;
- created_at/last_seen_at/expires_at non-null UTCDateTime;
- invalidated_at nullable UTCDateTime;
- no raw bearer token;
- no raw CSRF token;
- no cookie value;
- no password material;
- no permission snapshot;
- no admin snapshot;
- no JWT fields;
- index user_id if useful.

Avoid IP/user-agent persistence unless a frozen requirement explicitly requires it.

# 11. Session token generation/hashing

Generate raw session token server-side using `secrets` with >=256 bits entropy, e.g. `secrets.token_urlsafe(32)`.

Requirements:
- never accept client-selected session ID;
- fresh token every successful login;
- raw token only in session cookie;
- not in response JSON;
- not logged;
- not persisted.

Persist deterministic SHA-256 lowercase hex digest for indexed lookup.

Do not use Argon2 for random session-token lookup.

# 12. CSRF design

Use distinct random CSRF token.

Recommended browser contract:

```text
ipsp_session cookie: HttpOnly raw bearer token
ipsp_csrf cookie: readable by same-origin JS
X-CSRF-Token header: copied from CSRF cookie
database: csrf_token_hash only
```

Authenticated state-changing validation:
1. valid session cookie;
2. CSRF cookie present;
3. CSRF header present;
4. cookie/header equal using constant-time compare;
5. SHA-256 hash matches stored csrf_token_hash;
6. session valid, active, unexpired.

At least 256-bit CSRF entropy.

Never reuse session token as CSRF token.
Never persist/log raw CSRF token.

# 13. Cookie security

Centralize set/clear helpers.

Session cookie:
- configured name
- HttpOnly=True
- Secure=True in production
- SameSite config, default lax
- Path=/
- no broad Domain
- expiry/max-age aligned with session

CSRF cookie:
- configured name
- HttpOnly=False
- same Secure/SameSite/Path/expiry policy

Logout/password change clear both.

No auth token in localStorage/sessionStorage/URL/body.

# 14. Repositories

Create concrete sync repos under `backend/ipsp/repositories/`, no generic BaseRepository.

Minimal:
- UserRepository: get id/username, count users, add, mutate auth state.
- RoleRepository: get name, add, bootstrap only.
- UserSessionRepository: add, get by token hash, invalidate one, invalidate all by user, update last_seen.

Rules:
- receive canonical Session;
- SQLAlchemy 2.x select/execute/scalars;
- no Session.query;
- repositories do not commit;
- AuthService owns transaction boundaries.

# 15. AuthService

Create under `backend/ipsp/auth/`.

Service operations may include:

```text
login
authenticate_session
validate_csrf
logout
change_password
invalidate_all_user_sessions
bootstrap_admin
```

No FastAPI types in domain service.
No SQL in routes.
No permission enforcement.

# 16. Login API

`POST /api/v1/auth/login`

Request Pydantic schema:
- username
- password using `SecretStr` or equivalent safe representation.

Algorithm:
1. lookup user;
2. unknown -> dummy Argon2 verify;
3. disabled -> generic failure;
4. active lockout -> generic failure;
5. verify password;
6. failed verify:
   - increment failed_login_count;
   - threshold reached => locked_until now + configured duration;
   - generic auth failure;
7. successful:
   - reset failed count;
   - clear locked_until;
   - update last_login_at;
   - rehash if pwdlib recommends;
   - invalidate existing IPSP session cookie if present;
   - issue fresh session token;
   - issue fresh CSRF token;
   - persist only hashes;
   - generate fresh non-secret session_correlation_id;
   - fixed absolute expiry;
   - set cookies;
   - return safe identity response.

Every successful login issues a new bearer token.

# 17. Generic login failure

Use one external error such as:

```text
AUTH-INVALID_CREDENTIALS
Authentication failed.
```

Same public status/message/shape for:
- unknown username
- wrong password
- disabled account
- locked account

Do not expose failed count/lockout timestamp.

# 18. Lockout semantics

Defaults:
- threshold 5
- lockout 15 min

Rules:
- failed password increments;
- threshold sets locked_until;
- locked user denied;
- after expiry correct password can login;
- successful login resets count/lock;
- disabled user always denied.

No IP-distributed rate limiter this phase.

# 19. Session authentication

Input only configured HttpOnly session cookie.

Validate:
1. cookie exists;
2. hash;
3. session exists;
4. invalidated_at is None;
5. now < expires_at;
6. user exists;
7. user active.

Invalid:
- safe AUTH error;
- expired session may be invalidated;
- disabled user's active sessions should be invalidated.

Valid:
- update last_seen_at;
- return typed principal with safe identity:
  user_id, username, display_name, email, role_id/name, must_change_password,
  session_correlation_id, expiry.
- no password/token/csrf hashes.

Role is context only, not authority.

# 20. /auth/me

`GET /api/v1/auth/me`

Valid session required.

Safe response may include:
- id
- username
- display_name
- email
- role_id
- role_name
- must_change_password
- session_expires_at

Do not return:
- password_hash
- token_hash
- raw session
- csrf hash
- permissions
- is_admin

Set `Cache-Control: no-store`.

# 21. Logout

`POST /api/v1/auth/logout`

Requirements:
- valid session;
- valid CSRF;
- invalidate current server session;
- set invalidated_at;
- clear session + CSRF cookies;
- no raw token logging;
- 204 acceptable.

# 22. Change password

`POST /api/v1/auth/change-password`

Requirements:
- valid session;
- valid CSRF;
- SecretStr current/new passwords;
- verify current password;
- hash new Argon2id;
- password_changed_at=now;
- must_change_password=False;
- reset failed-login/lock state as appropriate;
- invalidate all sessions for user including current;
- clear cookies;
- fresh login required afterward;
- safe failure for wrong current password.

No password reset without current password.

# 23. Role-change invalidation primitive

Expose:

```text
invalidate_all_user_sessions(user_id, timestamp)
```

Phase 1F will call it after role/privilege changes.

Test:
- multiple sessions for user A invalidated;
- user B unaffected.

Do not implement role changes now.

# 24. Disabled-user enforcement

Test:
- disabled user cannot login;
- disabling authenticated user blocks old session;
- rejected session invalidated;
- public error does not reveal disabled state.

No disable-user API this phase.

# 25. Session fixation

Test:
- login never accepts client-selected session ID;
- each successful login token differs;
- login with existing valid IPSP session invalidates old session;
- only hash persists;
- raw token absent from all DB text fields.

# 26. Raw token at rest

Prove:
- token_hash != raw;
- token_hash == expected SHA-256;
- raw session absent from DB;
- raw CSRF absent from DB;
- raw values absent from logs.

# 27. Auth errors

Reuse `IPSPError`.

Suitable codes:
- AUTH-INVALID_CREDENTIALS
- AUTH-SESSION_REQUIRED
- AUTH-SESSION_INVALID
- AUTH-PASSWORD_INVALID
- AUTHZ-CSRF_INVALID
- AUTH-BOOTSTRAP_UNAVAILABLE

AUTH -> 401, AUTHZ -> 403.

No FastAPI HTTPException from domain service.
No secret/internal details.

# 28. FastAPI auth dependencies

Create reusable dependencies, e.g. `backend/ipsp/api/dependencies/auth.py`.

`require_authenticated_session`:
- read session cookie;
- call auth service;
- return principal;
- populate safe request state:
  - user_id
  - session_correlation_id
  - resolved role id/name
- no permission enforcement.

`require_csrf`:
- read CSRF cookie/header;
- call auth service validator;
- safe 403 on failure.

# 29. API schemas

Under `backend/ipsp/api/schemas/`.

At minimum:
- LoginRequest
- AuthenticatedIdentityResponse
- ChangePasswordRequest

Use `SecretStr` for password fields.

Test plaintext password marker absent from repr/validation output.

No ORM response leakage.

# 30. Auth routes

Routes only under `backend/ipsp/api/routes/`.

Register centrally.

Required:
```text
POST /api/v1/auth/login
GET  /api/v1/auth/me
POST /api/v1/auth/logout
POST /api/v1/auth/change-password
```

Thin routes only.

# 31. CSRF scope

Require CSRF on:
- POST /auth/logout
- POST /auth/change-password

Login is unauthenticated and does not require an existing authenticated CSRF token.
GET /auth/me does not require CSRF.

Reusable dependency should work for future protected POST/PUT/PATCH/DELETE routes.

# 32. First-admin bootstrap CLI

Implement preferred CLI, e.g.:
- `backend/ipsp/cli/admin.py`
- optional thin `scripts/create_admin.py`

Requirements:
- DB already at current migration head;
- CLI does not run migrations;
- refuse if any user exists;
- ensure/create canonical `Admin` and `User` Role rows;
- create first user assigned Admin;
- create no role_permissions rows;
- no RBAC;
- password via `getpass`;
- confirmation via getpass;
- no plaintext normal command-line password arg;
- no echo;
- production PasswordService hashing;
- created_by=None;
- must_change_password=False;
- no default/generated printed password;
- safe refusal on second bootstrap.

Keep internal testable bootstrap function accepting in-memory password.

Test:
- migrated empty DB bootstrap succeeds;
- Admin/User roles exist;
- first user Admin;
- Argon2id hash verifies;
- no role_permissions rows;
- second bootstrap refused;
- password absent stdout/stderr/logs.

# 33. Migration

Create new migration under sole history.

Expected:

```text
20260811_01
    ↓
20260811_02
    ↓
20260811_03
```

Use `20260811_03` unless repository convention requires equivalent deterministic ID.

Migration:
- creates only user_sessions;
- correct unique/index/FK constraints;
- UTCDateTime;
- no seed data;
- downgrade to 20260811_02;
- re-upgrade;
- alembic check clean.

# 34. Migration lifecycle tests

Isolated temp DB:

```text
empty -> 20260811_02 -> Phase1E head -> 20260811_02 -> Phase1E head
```

Verify:
- one Alembic head;
- correct current revision;
- expected five ORM tables;
- downgrade removes only user_sessions;
- Phase1D tables remain;
- re-upgrade restores;
- alembic check passes;
- readiness at Phase1E head 200;
- DB at 20260811_02 => 503 SYS-MIGRATION-REQUIRED;
- liveness 200.

# 35. Session schema tests

Verify migrated SQLite:
- exact five-table ORM allowlist;
- token_hash unique/non-null;
- csrf_token_hash non-null;
- session_correlation_id unique/non-null;
- user_id FK;
- UTC timestamp nullability;
- invalidated_at nullable;
- no raw token/JWT/refresh/permission/admin snapshot fields;
- FK invalid user rejected.

# 36. Password tests

Test:
- hash != plaintext;
- Argon2id;
- correct verify;
- wrong fails;
- Unicode works;
- marker absent repr/log/errors;
- no bcrypt new-hash path;
- rehash/update path where deterministic;
- unknown-user dummy verify path.

# 37. Login integration tests

Through TestClient:
- valid login 200;
- session cookie set;
- session HttpOnly;
- CSRF cookie set/readable;
- raw session absent JSON;
- identity safe;
- wrong/unknown/disabled/locked => same generic 401;
- failed count increments;
- threshold locks;
- lock expiry + correct password works;
- success clears count/lock;
- last_login_at updated;
- each login gets fresh token;
- previous same-browser session invalidated;
- Cache-Control no-store.

# 38. Cookie tests

Production:
- cookie_secure=False rejected;
- session Secure;
- csrf Secure;
- session HttpOnly;
- csrf not HttpOnly;
- SameSite correct.

Development:
- explicit cookie_secure=false allowed for localhost tests.

Do not weaken production for tests.

# 39. /auth/me tests

- valid 200;
- safe fields only;
- role identity okay;
- no permissions/hash/raw token/csrf hash;
- invalid/unknown/expired/invalidated token 401;
- disabled existing session 401 + invalidation;
- last_seen advances;
- Cache-Control no-store.

# 40. CSRF tests

For logout/change-password:
- valid cookie/header succeeds;
- missing cookie 403;
- missing header 403;
- mismatch 403;
- header/cookie match but stored hash mismatch 403;
- CSRF from another session 403;
- raw marker absent logs.

# 41. Logout tests

- valid session+CSRF succeeds;
- invalidated_at set;
- subsequent me 401;
- both cookies cleared;
- no token leak;
- other user session unaffected.

# 42. Password-change tests

- correct current + CSRF succeeds;
- hash changes;
- new verifies;
- old fails;
- password_changed_at advances;
- must_change_password false;
- all user's sessions invalidated;
- other user's sessions unaffected;
- cookies cleared;
- old session fails;
- wrong current fails safely and leaves password unchanged;
- markers absent.

# 43. Session UTC/expiry

Use existing UTCDateTime.

Test aware UTC reads, expiry calculation, expired denial, no naive writes, nullable invalidated_at.

No second datetime type.

# 44. Session correlation

Generate independently from bearer token.

Requirements:
- random/UUID non-secret;
- unique;
- may go on request.state;
- not derived from/truncated bearer token;
- raw cookie never substitutes.

Test differs from raw token/hash and survives authenticated request context.

# 45. Logging/redaction

Use markers:
- DO_NOT_LEAK_LOGIN_PASSWORD
- DO_NOT_LEAK_SESSION_TOKEN
- DO_NOT_LEAK_CSRF_TOKEN

Exercise bad/success login, me, CSRF fail, logout, password change.

Assert absent from:
- structured/request/error logs
- client errors
- Pydantic repr
- DB raw-token-forbidden fields

Do not log password hashes.

Full durable audit stays Phase 1G.

# 46. Error-handler interaction

Preserve existing stable error envelope.

Do not expose ORM/SQLite errors, lockout timestamp, username existence, password/token values.

# 47. Composition

Extend explicit immutable composition with auth services.

No global mutable AuthService.
No DB work at module import.
No automatic migrations.
No random app-wide production secret.

Avoid generating expensive dummy Argon2 hash per request.

# 48. Conformance evolution

Phase1D guards must evolve.

Expected ORM allowlist:

```text
permissions
role_permissions
roles
user_sessions
users
```

Allowed now:
- pwdlib/argon2 only in auth password dependency/implementation;
- user_sessions;
- auth service/routes/schemas/dependencies/repositories.

Still prohibit:
- persisted is_admin/admin bypass;
- RBACService/permission enforcement;
- role-name authorization shortcuts;
- JWT/python-jose/PyJWT;
- bcrypt/passlib;
- raw token DB columns;
- refresh-token field/table;
- Session.query;
- AsyncSession/create_async_engine/aiosqlite;
- production create_all;
- duplicate ORM/Alembic roots;
- Redis/Celery;
- HTTP clients;
- Streamlit;
- React/Vue/Angular;
- runtime CDN;
- benchmark contamination.

# 49. No RBAC in Phase 1E

Phase1E answers:
```text
Who is this user?
Is session valid?
Is request CSRF-valid?
```

Phase1F answers:
```text
May this user perform this action?
```

Phase1E may return role name/id as identity context only.

Do not inspect role_permissions to allow/deny.
Do not expose permission list.
Do not authorize based on role name Admin.

# 50. Bootstrap role names

Bootstrap may ensure Role rows:
- Admin
- User

But never:
```python
if role.name == "Admin": allow
```

No permission mappings this phase.

# 51. Readiness

Do not redesign.

- Phase1E head -> ready 200
- Phase1D head 20260811_02 -> 503 SYS-MIGRATION-REQUIRED
- FK disabled -> 503
- liveness -> 200

Do not require existence of admin or sessions for readiness.

# 52. .env/config docs

Update `.env.example` and config docs with non-secret auth settings.

Development example may show:
```text
IPSP_AUTH__SESSION_TTL_MINUTES=480
IPSP_AUTH__FAILED_LOGIN_THRESHOLD=5
IPSP_AUTH__LOCKOUT_MINUTES=15
IPSP_AUTH__SESSION_COOKIE_NAME=ipsp_session
IPSP_AUTH__CSRF_COOKIE_NAME=ipsp_csrf
IPSP_AUTH__CSRF_HEADER_NAME=X-CSRF-Token
IPSP_AUTH__COOKIE_SECURE=false
IPSP_AUTH__COOKIE_SAMESITE=lax
```

Clearly mark cookie_secure=false as localhost/development only. Production must fail closed.

No secret/password/token values in env example.

# 53. Clean lock verification

Because pwdlib[argon2] is new, regenerate/verify lock.

Report:
- direct constraint/version;
- exact resolved pwdlib;
- Argon2 transitives;
- other changed transitives;
- Python version;
- clean install result.

Run in clean env:
```text
pip check
pytest
ruff check .
ruff format --check .
mypy backend/ipsp
python -m compileall -q backend tests
```

Remove disposable clean env afterward.

# 54. Full gates

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

Migration smoke isolated:
```text
alembic heads
alembic upgrade head
alembic current
alembic check
alembic downgrade 20260811_02
alembic upgrade head
```

Never use real default DB.

# 55. Documentation

Update:
- `.env.example`
- `config/README.md`
- `database/migrations/README.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`

Record:
`Phase 1E — Authentication & Server-Side Session Security`

Document Argon2id, user_sessions, hashing, cookies, CSRF, lockout, APIs, disabled-user behavior, invalidation, bootstrap admin, tests.

Explicitly say RBAC enforcement remains Phase1F.

Do not mark Phase1/v0.1.0 complete.

# 56. Git discipline

Before:
```text
git status --short
git rev-parse HEAD
```

After:
```text
git status --short
git diff --stat
git diff --check
```

Do not auto commit/push.

Do not track DB/WAL/SHM/env/password/token dumps/venvs/caches/logs/archives.

# 57. Phase 1E acceptance gate

PASS only if:

Passwords:
- pwdlib[argon2]
- Argon2id
- plaintext never persisted
- no bcrypt fallback
- dummy unknown-user verify
- no leaks

Schema:
- exactly user_sessions new table
- five-table allowlist
- no raw session/csrf columns
- correct unique/FK/UTC fields
- migration 03 from 02
- lifecycle/check passes

Sessions:
- >=256-bit opaque token
- new token each login
- old same-browser invalidated
- SHA-256 stored
- raw only HttpOnly cookie
- expiry
- last_seen
- logout invalidation
- password change all-session invalidation
- disabled-user rejection
- future role-change invalidation primitive

CSRF:
- independent >=256-bit token
- hash-only storage
- readable cookie + header
- logout/change-password protected
- 403 failures
- no leaks

Cookies:
- session HttpOnly
- production Secure mandatory
- explicit localhost exception
- safe SameSite
- clear on logout/password change
- no JSON/localStorage auth token design

Lockout:
- threshold/count/locked_until
- expiry reset behavior
- generic external errors

API:
- login/me/logout/change-password
- thin routes
- separate schemas
- no permissions

Bootstrap:
- first-admin CLI
- getpass
- no default password
- Admin/User role rows
- no role_permissions
- second run refused

Architecture:
- no is_admin
- no Admin-name authorization
- no RBACService
- no JWT
- no passlib/bcrypt
- no async SQLAlchemy
- no create_all
- one Alembic root
- no Streamlit/framework
- no Redis/Celery/network
- no contamination

Quality:
- pytest/Ruff/mypy/compileall/pip/diff pass
- clean lock verification passes
- docs accurate

# 58. Mandatory Codex final report

## A. Starting state
SHA, branch, initial status.

## B. Files created
Every file.

## C. Files modified
Every file.

## D. Dependencies
pwdlib constraint/version, Argon2 transitives, lock changes, clean Python/env verification.

## E. Auth configuration
Env names/defaults/production fail-closed/development exception.

## F. Password implementation
Argon2id proof, verify/rehash, dummy verify, no bcrypt/passlib.

## G. UserSession schema
Columns, PK/FK, unique/index, nullability, UTC, raw-token absence.

## H. Migration
Revision/parent/upgrade/current/head/check/downgrade/re-upgrade/table allowlist.

## I. Repository/service architecture
Repos, transaction ownership, AuthService, no RBAC.

## J. Session-token security
Entropy, hash, raw persistence proof, fixation/rotation, expiry, invalidation.

## K. Cookie/CSRF
Flags/model/prod-local behavior/403/cookie clearing.

## L. Login/lockout
Success/generic failures/count/threshold/expiry/reset/disabled.

## M. Auth API
login/me/logout/change-password.

## N. Password change
Hash/timestamp/must_change/all-session invalidation/other-user isolation.

## O. Bootstrap admin
Migration-head requirement, empty-user requirement, roles, admin creation, password handling, second-run refusal, no mappings.

## P. Leak evidence
Markers and absence from logs/responses/repr/DB.

## Q. Readiness
Phase1E head 200, Phase1D head 503, liveness 200.

## R. Tests
Exact passed/failed/skipped/warnings.

## S. Quality gates
compileall/Ruff/mypy/pip/diff.

## T. Architecture/conformance
ORM allowlist, duplicate ownership, is_admin, RBAC enforcement, JWT, bcrypt/passlib, Session.query, async DB, create_all, Alembic roots, raw-token fields, Streamlit/framework/CDN, Redis/Celery, HTTP, contamination.

## U. Runtime artifacts
DB/WAL/SHM, token/password dumps, clean venvs, caches, logs.

## V. Git state
Final status + diff stat.

## W. Deviations / unresolved issues
If none: `None`

## X. Gate result

End exactly with:

`Phase 1E: PASS — ready for independent review before Phase 1F`

or

`Phase 1E: FAIL — Phase 1F blocked`

Do not begin Phase 1F.
