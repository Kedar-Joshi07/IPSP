# Configuration

`ipsp.config.Settings` is the sole process-configuration source. It loads validated, non-secret
values from `IPSP_`-prefixed environment variables or a local, ignored `.env` file.

Phase 1B separates three concepts:

- runtime settings such as environment, bind address, paths, logging, and theme;
- `features`, which describe platform feature availability and never grant permission;
- `outbound`, which independently enforces Internet, remote-LLM, provider, download, update-check,
  and remote-transmission policy.

Phase 1E adds non-secret `auth` policy for fixed session lifetime, failed-login lockout, cookie and
CSRF names, and browser cookie flags. Defaults are 480 session minutes, five failed attempts, a
15-minute lockout, `ipsp_session`, `ipsp_csrf`, `X-CSRF-Token`, Secure cookies, and SameSite `lax`.
Canonical variables are `IPSP_AUTH__SESSION_TTL_MINUTES`,
`IPSP_AUTH__FAILED_LOGIN_THRESHOLD`, `IPSP_AUTH__LOCKOUT_MINUTES`,
`IPSP_AUTH__SESSION_COOKIE_NAME`, `IPSP_AUTH__CSRF_COOKIE_NAME`,
`IPSP_AUTH__CSRF_HEADER_NAME`, `IPSP_AUTH__COOKIE_SECURE`, and
`IPSP_AUTH__COOKIE_SAMESITE`.

Production configuration fails closed when `IPSP_AUTH__COOKIE_SECURE=false`. That override is
permitted only as an explicit development/localhost HTTP choice; HTTPS and Secure cookies remain the
default. Passwords, raw session tokens, and CSRF tokens are runtime credentials and never Settings
or environment-example fields.

Nested settings use `__` as the environment delimiter. Canonical examples include:

```text
IPSP_FEATURES__REMOTE_LLM_ENABLED=false
IPSP_OUTBOUND__INTERNET_ENABLED=false
IPSP_OUTBOUND__REMOTE_LLM_ENABLED=false
IPSP_OUTBOUND__ALLOWED_REMOTE_PROVIDERS=[]
IPSP_OUTBOUND__DEFAULT_REMOTE_TRANSMISSION=remote_disabled
IPSP_SECRETS__PROVIDER=environment
```

The Phase 1A variables `IPSP_INTERNET_ENABLED` and `IPSP_REMOTE_LLM_ENABLED` are retired. Use the
nested canonical variables above; remote feature availability and remote outbound permission must
be configured independently.

## Secrets

Secret values are never fields on `Settings`. A safe `SecretRef` identifies provider metadata and a
specific external key, while `EnvironmentSecretProvider` resolves only that requested environment
entry into a redacted `SecretValue`. Required lookups fail closed and no fallback credential is
generated.

Environment injection is the approved production source implemented in Phase 1B. Protected OS,
vault, and cloud providers remain future implementations behind the same `SecretProvider` contract;
no unfrozen keychain or vault technology is selected here.

`.env.example` contains non-secret defaults only. Never commit a real `.env`, credential, bearer
token, cookie, or resolved secret value.

## Structured observability

Phase 1G uses `IPSP_LOG_LEVEL` and `IPSP_LOG_DIR` for two local structured sinks: one console stream
and `<log_dir>/ipsp-runtime.jsonl`, a UTF-8 JSONL file rotating at 10 MiB with five backups. Repeated
application construction replaces only IPSP-owned handlers, closes the old file sink, and never
configures a network exporter. Runtime JSONL files and rotations are operational artifacts and must
not be committed.

High-volume application, request, frontend, and performance events remain in the rotating runtime
sink. SQLite stores only explicitly selected audit/security events through the append-only
`audit_events` repository. Both forms share the same sanitized event envelope and non-secret
request/trace/session correlation fields; neither accepts raw passwords, hashes, cookies, bearer or
CSRF tokens, Authorization headers, request bodies, or exception messages/locals.

## Local RBAC provisioning

Phase 1F provisioning is explicit and never runs at application startup or readiness. After applying
the canonical Alembic migrations, use `ipsp-create-admin` for a fresh installation with zero users.
It creates the first Admin identity and provisions the core permission catalog through explicit
`role_permissions` mappings.

For an existing installation, run `ipsp-sync-rbac`. It requires the database to already be at the
current migration head, ensures the Admin/User roles and the 13 core permissions, adds missing Admin
mappings, preserves all custom roles/permissions/mappings, and deletes nothing. User receives no
automatic permission grants. Synchronization is idempotent; any newly expanded Admin privileges
invalidate existing Admin-user sessions so affected users must authenticate again.
