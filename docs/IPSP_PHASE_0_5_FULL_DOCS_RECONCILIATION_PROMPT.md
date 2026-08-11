# GitHub Copilot — Phase 0.5 Full Documentation Reconciliation Prompt

You are working inside the IPSP v1.0 repository.

The complete `docs/` folder has now been independently reviewed. The underlying IPSP architecture is approved, but the generated Phase 0 implementation plan contains several contradictions with the numbered specifications.

## Absolute instruction

**DO NOT WRITE PRODUCTION APPLICATION CODE IN THIS RUN.**

This is a documentation/architecture reconciliation pass only.

## Read first, in this order

1. `AGENTS.md`
2. `.github/copilot-instructions.md`
3. `docs/00_SCOPE_FREEZE.md`
4. `docs/01_PROJECT_SPEC.md`
5. `docs/02_PRODUCT_REQUIREMENTS.md`
6. `docs/03_ARCHITECTURE.md`
7. `docs/04_PROJECT_STRUCTURE.md`
8. `docs/05_UI_UX_SPEC.md`
9. `docs/06_UI_DESIGN_SYSTEM.md`
10. `docs/15_TRUST_AND_VALIDATION_SPEC.md`
11. `docs/18_SECURITY_RBAC_SPEC.md`
12. `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
13. `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
14. `docs/24_JOB_PROCESSING_SPEC.md`
15. `docs/27_SQLITE_SCHEMA_SPEC.md`
16. `docs/28_REST_API_CONTRACT.md`
17. `docs/29_TEST_STRATEGY.md`
18. `docs/30_ACCEPTANCE_CRITERIA.md`
19. `docs/31_IMPLEMENTATION_PROGRESS.md`
20. `docs/32_DECISION_LOG.md`
21. `docs/35_CONFIGURATION_SPEC.md`
22. `docs/37_SYSTEM_HEALTH_SPEC.md`
23. `docs/40_ANTI_CONTAMINATION.md`
24. `docs/PHASE_0_IMPLEMENTATION_PLAN.md`
25. `docs/PHASE_0_FULL_DOCS_AUDIT.md`
26. every remaining Markdown file under `docs/`

## Governing rule

Where the current `PHASE_0_IMPLEMENTATION_PLAN.md` conflicts with a locked numbered specification, do not preserve the plan merely because it is more detailed. Correct the plan so it implements the approved architecture.

## Mandatory corrections

### Authorization
- Eliminate persisted `is_admin` as an authorization authority.
- Use Role -> Permission as the sole authorization authority.
- V1.0 can use one `role_id` per user because only Admin/User roles are required.
- If an `is_admin` convenience value appears in an API response, it must be computed from role/permissions, never persisted or checked for authorization.

### ORM/API contracts
- One SQLAlchemy ORM definition per entity.
- Pydantic schemas are separate from ORM entities.
- Do not define `User`, `Role`, `Permission`, `AuditEvent`, etc. as ORM classes in more than one module.

### SQLAlchemy execution model
- Use synchronous SQLAlchemy 2.x for the lightweight SQLite control plane unless a Decision Log entry explicitly chooses a fully asynchronous alternative.
- Do not use synchronous Session operations inside `async def`.
- Do not use legacy `Session.query()` patterns.
- Use SQLAlchemy 2.x select/execute/scalars style.
- Heavy data/ML/simulation/report work belongs to jobs.

### Dependencies
- Delete stale hard-pinned example versions from the Phase 0 plan.
- Re-resolve maintained compatible versions during implementation.
- Direct dependencies belong in `pyproject.toml`; use a lock/constraints mechanism for reproducibility.
- `sqlite3` is not a pip dependency.
- Prefer `pwdlib[argon2]` for new Argon2id password hashes.
- Do not add JWT/python-jose for browser authentication unless a separate token API requirement is introduced.
- Do not add bcrypt fallback for newly created hashes unless legacy-hash migration becomes a requirement.

### Sessions and auth security
- Server-side opaque sessions.
- Generate/rotate the session token on successful login.
- Invalidate/rotate on password change and role/privilege change.
- Never log raw bearer session tokens.
- Prefer hashed session-token storage.
- HttpOnly cookies.
- Secure in HTTPS/production, with explicit localhost dev behavior.
- Suitable SameSite + CSRF for browser state-changing requests.
- Failed login throttling/temporary lockout.
- Timezone-aware UTC timestamps.

### User schema
Email is optional unless another approved feature requires it.

Document at minimum:
`id, username, display_name, email nullable, password_hash, role_id, is_active, must_change_password, failed_login_count, locked_until, last_login_at, password_changed_at, created_at, created_by, updated_at`.

No independent `is_admin`.

### Secrets
- Do not generate a new production secret automatically on each startup.
- Production fails closed if required secrets are absent.
- Local development bootstrap may be explicit.
- SecretProvider/environment/protected OS storage provides stable secrets.
- No ordinary plaintext provider secrets in SQLite or logs.

### Frontend/offline
- No runtime CDN dependency.
- Plotly.js and any other third-party browser bundle is explicitly versioned and vendored under `frontend/assets/vendor/`.
- Track version/license.
- Runtime external assets must obey OutboundPolicy.

### Themes
Foundation v0.1.0 must include:
- shared design tokens
- dark theme tokens
- light theme tokens
- theme switch mechanism
- persistence mechanism

Full dynamic page implementation can remain a later UI milestone, but the light-theme architecture is not postponed as a retrofit.

### Versioning
- `datasets` = logical identity.
- `dataset_versions` = immutable versions.
- Semantic manifests/semantic versions are immutable once referenced.
- Model versions/artifacts are immutable registry records.
- Simulation runs reference exact dataset version, semantic version, model/capability version, seed, and effective non-secret configuration snapshot/hash.
- Do not use mutable version labels as the only foreign reference.

### Multi-table
- Remove mutable `is_multi_table` source-of-truth.
- Derive from `dataset_tables`.

### Migrations
- Keep one Alembic history only.
- Use the canonical repository migration root selected by project structure.
- Remove duplicate migration locations from the plan.

### Route ownership
- Use one canonical `backend/ipsp/api/routes/` location.
- Domain packages contain services/policies/schemas; routes remain thin.

### Observability
Replace raw `session_id` in event-envelope documentation with a safe `session_correlation_id`.

Minimum event envelope:
- timestamp_utc
- event_id
- trace_id
- request_id
- session_correlation_id
- user_id
- resolved role
- project/dataset/version/run/model references as applicable
- component
- action
- status
- duration_ms
- severity
- error_code
- resource_type/resource_id
- sanitized metadata

Durable audit/security records may live in SQLite. High-volume runtime/application logs use structured rotating files or another sink rather than SQLite as the complete log warehouse.

### Sampling
Do not infer full source-dataset insufficiency from a 500-row random sample.

But if a model is actually trained on a 500-row sample, its sample size still matters to that model's validation.

Keep:
`DISCOVERED -> VALIDATING -> VALIDATED -> ENABLED`.

### Negative finance values
A negative value is not automatically:
- invalid,
- a business exception,
- or anomalous.

Classify according to intrinsic constraints, confirmed semantic/business rules, and evidence.

### Jobs
Bring job contracts into v0.1.0 foundation:
- JobBackend
- JobService
- JobRepository
- JobStatus
- JobType
- progress/cancellation/retry/error contract

Do not make Redis/Celery required in V1.0 foundation.

### Health
Separate:
- liveness
- readiness
- rich Admin system health

Do not use bare exception handlers or expose raw diagnostics.

## Documents that must be updated where needed

At minimum inspect and reconcile:

- `docs/04_PROJECT_STRUCTURE.md`
- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/24_JOB_PROCESSING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/29_TEST_STRATEGY.md`
- `docs/30_ACCEPTANCE_CRITERIA.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Do not modify files merely to create churn. Change only where required to make the architecture internally consistent.

## Progress state

Update `31_IMPLEMENTATION_PROGRESS.md` to introduce:

`Phase 0.5 — Architecture correction + documentation reconciliation`

Phase 1 must remain BLOCKED until Phase 0.5 verification passes.

## Create reconciliation report

Create:

`docs/PHASE_0_5_RECONCILIATION_REPORT.md`

For every audit finding:
- finding ID
- affected files
- exact resolution
- verification search performed
- result: PASS/FAIL
- unresolved questions, if any

## Documentation-wide verification searches

Before completion, search all Markdown files for:
- `is_admin`
- duplicate ORM definitions
- `async def` around synchronous Session patterns
- `Session.query`
- stale exact dependency pins
- `passlib`
- `python-jose`
- unnecessary bcrypt fallback
- `sqlite3` as dependency
- CDN / `latest` browser dependencies
- regenerated production secret defaults
- duplicate migration locations
- duplicate auth router ownership
- mutable dataset version assumptions
- `is_multi_table`
- raw session IDs in logging/audit
- Phase 7-only light-theme foundation
- Redis/Celery as required early dependencies
- incorrect 500-row sample-size conclusions
- universal non-negative finance rules
- `Phase 1 ready` before Phase 0.5 completion

Also run a benchmark-contamination scan against generic production architecture documentation.

## Completion conditions

Phase 0.5 PASS only if:
- one authorization authority exists;
- one ORM ownership pattern exists;
- one DB execution model exists;
- one migration history exists;
- one API route ownership pattern exists;
- offline frontend dependency policy is explicit;
- both theme foundations are in v0.1.0;
- immutable version-reference design is explicit;
- session lifecycle and secret policy are safe;
- observability does not log bearer session IDs;
- job contracts exist in the foundation;
- health is split into liveness/readiness/admin diagnostics;
- no production code has been written;
- no benchmark-specific business logic has entered core documentation.

## Final response

Report:
1. files created
2. files modified
3. decisions added/changed
4. verification searches
5. unresolved questions
6. Phase 0.5 PASS/FAIL
7. whether Phase 1 may safely start

Do not start Phase 1 implementation in this run.
