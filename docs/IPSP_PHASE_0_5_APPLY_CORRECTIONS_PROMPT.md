# GitHub Copilot Prompt — Phase 0.5 APPLY CORRECTIONS (Do Not Re-Audit)

You are working in the IPSP v1.0 repository.

## Important correction to the previous run

The previous Phase 0.5 run only created audit/reconciliation reports. It **did not apply the required corrections** to the existing specifications or to `PHASE_0_IMPLEMENTATION_PLAN.md`.

This run is therefore an **EDITING / RECONCILIATION EXECUTION PASS**, not another audit.

# ABSOLUTE RULES

1. **DO NOT write production Python, HTML, CSS, JavaScript, SQL migrations, or application code.**
2. **DO modify the existing Markdown specification and plan files.**
3. Do not merely create another report saying what should be changed.
4. Do not stop after identifying issues.
5. Apply the corrections directly to the source documents.
6. Before finishing, produce a Git diff / changed-file list proving the required files were edited.
7. If `PHASE_0_IMPLEMENTATION_PLAN.md` is not modified in this run, the run is automatically **FAIL**.
8. If fewer than the necessary affected specification files are modified, explain why with exact evidence; otherwise the run is **FAIL**.

## Read first

Read completely:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/00_SCOPE_FREEZE.md`
- `docs/03_ARCHITECTURE.md`
- `docs/04_PROJECT_STRUCTURE.md`
- `docs/05_UI_UX_SPEC.md`
- `docs/06_UI_DESIGN_SYSTEM.md`
- `docs/15_TRUST_AND_VALIDATION_SPEC.md`
- `docs/18_SECURITY_RBAC_SPEC.md`
- `docs/19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `docs/22_OBSERVABILITY_AUDIT_SPEC.md`
- `docs/24_JOB_PROCESSING_SPEC.md`
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
- `docs/IPSP_PHASE_0_FULL_DOCS_AUDIT.md`
- `docs/PHASE_0_5_RECONCILIATION_REPORT.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

## Apply these decisions directly

### 1. Authorization
Edit the plan/specs so that:
- Role -> Permission is the only authorization authority.
- V1.0 may use one `role_id` per user.
- Remove persisted `is_admin`.
- Never authorize with `if user.is_admin`.
- A convenience API property may be computed from the resolved role only.

### 2. ORM / Pydantic separation
Edit the structure/plan so that:
- SQLAlchemy ORM entities have one canonical ownership location.
- Pydantic request/response schemas are separate.
- No duplicate ORM definitions for User/Role/Permission/AuditEvent/etc.

Recommended:
- `backend/ipsp/database/models/`
- `backend/ipsp/api/schemas/`
- domain services under their domain packages.

### 3. Database execution model
Lock synchronous SQLAlchemy 2.x for the SQLite control plane:
- normal synchronous repository/service methods;
- `select()` / `Session.execute()` / `Session.scalars()`;
- no `Session.query()`;
- no fake `async def` around sync Session work;
- heavy work runs through jobs.

Record this decision in `32_DECISION_LOG.md`.

### 4. Dependency strategy
Remove stale exact package pins from the architecture plan.
State:
- current maintained compatible versions resolved at implementation time;
- direct dependencies in `pyproject.toml`;
- reproducible lock/constraints mechanism;
- `sqlite3` is stdlib, not pip dependency;
- prefer `pwdlib[argon2]`;
- no JWT/python-jose for ordinary browser login;
- no bcrypt fallback unless legacy-hash migration becomes an explicit feature.

### 5. User/auth schema
Update the schema/plan to include:
- id
- username unique
- display_name
- email nullable
- password_hash
- role_id
- is_active
- must_change_password
- failed_login_count
- locked_until
- last_login_at
- password_changed_at
- created_at
- created_by
- updated_at

No persisted `is_admin`.

### 6. Session lifecycle
Specify:
- opaque cryptographically random bearer token;
- rotate/new token on successful login;
- invalidate/rotate on password change and role/privilege changes;
- explicit expiry;
- preferably store only token hash;
- never log raw bearer token;
- HttpOnly;
- Secure for HTTPS/production with explicit local-dev behavior;
- appropriate SameSite plus CSRF for POST/PUT/PATCH/DELETE;
- failed login throttling/temporary lockout;
- timezone-aware UTC timestamps.

### 7. Secrets
Remove startup random-secret defaults.
Specify:
- production fails closed when required secrets are absent;
- stable secrets through SecretProvider/environment/protected storage;
- explicit dev bootstrap only;
- no plaintext secrets in SQLite/logs.

### 8. Frontend offline policy
Remove `latest CDN`.
Specify:
- pinned Plotly.js version;
- vendored local browser asset under `frontend/assets/vendor/`;
- version/license inventory;
- no runtime public CDN requirement.

### 9. Theme foundation
Move theme foundation into v0.1.0:
- shared semantic design tokens;
- dark theme tokens;
- light theme tokens;
- theme switch;
- persisted preference.

Later v0.7 may implement richer dynamic pages, but light-theme architecture is not postponed.

### 10. Immutable versioning
Ensure:
- `datasets` = logical identity;
- `dataset_versions` = immutable versions;
- semantic manifest versions immutable once referenced;
- model versions/artifacts immutable;
- simulation runs reference exact dataset/semantic/capability/model version records;
- persist seed and effective non-secret configuration snapshot/hash;
- no mutable version label as sole reproducibility reference.

### 11. Multi-table
Remove persisted `is_multi_table` as source of truth.
Derive multi-table status from `dataset_tables`.

### 12. Migrations
Use exactly one Alembic history.
Use the canonical repository migration root defined by the project structure.
Delete the duplicate migration-location guidance from the plan.

### 13. API route ownership
Use one canonical location such as:
`backend/ipsp/api/routes/`

Domain/auth packages own services/policies/schemas, not duplicate route modules.

### 14. Observability
Use `session_correlation_id`, never raw bearer `session_id`, in logs.

Minimum event envelope:
- timestamp_utc
- event_id
- trace_id
- request_id
- session_correlation_id
- user_id
- resolved role
- relevant project/dataset/version/model/run refs
- component
- action
- status
- duration_ms
- severity
- error_code
- resource_type
- resource_id
- sanitized metadata

Durable audit/security records may be stored in SQLite.
High-volume runtime/application logs go to structured rotating files or another log sink.

### 15. Sampling
Clarify:
- a 500-row random sample does not prove the source dataset is only 500 rows or that source categories are rare;
- if a model is actually trained on that sample, 500 is still its training sample size;
- capability lifecycle remains DISCOVERED -> VALIDATING -> VALIDATED -> ENABLED.

### 16. Negative financial values
State neutrally:
- intrinsic impossibility -> invalid;
- confirmed semantic/business rule violation -> violation;
- statistically unusual -> anomaly/warning;
- otherwise valid observation.
Negative values are not automatically errors or exceptions.

### 17. Jobs
Bring job contracts into v0.1.0 foundation:
- JobBackend
- JobService
- JobRepository
- JobStatus
- JobType
- progress/cancel/retry/error contracts

Do not require Redis/Celery in foundation.

### 18. Health
Document separate:
- liveness endpoint
- readiness endpoint
- rich Admin health diagnostics

No bare `except:` examples and no unsafe raw error exposure.

## Files that MUST be edited if the issue exists

At minimum, apply edits to the relevant subset of:

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
- `docs/34_CODING_STANDARDS.md`
- `docs/35_CONFIGURATION_SPEC.md`
- `docs/37_SYSTEM_HEALTH_SPEC.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`

Do not make cosmetic edits just to increase the changed-file count. Make substantive consistency edits where required.

## Required verification after edits

Run repository-wide searches and report actual results.

The corrected architecture must have:

- no persisted/authorization `is_admin`;
- no `Session.query(` implementation guidance;
- no mixed sync Session inside async repository/service guidance;
- no stale hard-pinned dependency block used as architectural authority;
- no `sqlite3` pip dependency;
- no required `python-jose` for server-session login;
- no required bcrypt fallback;
- no runtime CDN / `latest CDN` guidance;
- no startup auto-generated production secret;
- no duplicate migration roots;
- no duplicate auth route ownership;
- no mutable `is_multi_table` source-of-truth;
- no raw bearer session identifier in logs;
- no light-theme foundation deferred exclusively to v0.7;
- no Redis/Celery as foundation requirements;
- no universal non-negative finance rule.

## Update the reconciliation report

After applying edits, update:

`docs/PHASE_0_5_RECONCILIATION_REPORT.md`

For each prior finding:
- mark RESOLVED or UNRESOLVED;
- name exact files modified;
- summarize exact change;
- show verification evidence.

Do not leave the report saying "IN PROGRESS" if all corrections are actually complete.

## Update progress

`docs/31_IMPLEMENTATION_PROGRESS.md`:

Only mark Phase 0.5 PASS when all verification gates pass.

Only then set Phase 1 to READY.

## Mandatory final output

Your response must contain:

1. `git status --short` (or equivalent changed-file list)
2. `git diff --stat`
3. list of files actually modified
4. key decisions applied
5. verification-search results
6. unresolved issues
7. Phase 0.5 PASS/FAIL
8. Phase 1 READY/BLOCKED

### Automatic failure conditions
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md` unchanged
- only reports/progress files changed
- no substantive spec files changed
- contradictions remain but Phase 0.5 marked PASS
- production code created

Do not perform another audit-only pass. Apply the corrections now.
