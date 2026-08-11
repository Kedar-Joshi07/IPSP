# IPSP v1.0 — Full Docs Folder Cross-Document Audit

> Historical pre-correction audit. Its findings were resolved by the completed Phase 0.5 execution recorded in `PHASE_0_5_RECONCILIATION_REPORT.md`; descriptions of the former state below are not current implementation guidance.

**Audit scope:** `docs.zip` supplied after the first GitHub Copilot planning run.  
**Files inspected:** 42 Markdown files (41 numbered specifications plus `PHASE_0_IMPLEMENTATION_PLAN.md`).  
**Purpose:** Determine whether Phase 1 production implementation may safely begin.

## Executive verdict

**Result: CONDITIONAL FAIL for Phase 1 start.**

The specification set is substantially stronger and more internally consistent than the generated `PHASE_0_IMPLEMENTATION_PLAN.md`. The core IPSP architecture is not drifting and does not need redesign.

The main problem is that the Phase 0 implementation plan introduces conventional implementation shortcuts that contradict or weaken the higher-level specifications. A small number of specification files also need clarification so Copilot has only one authoritative answer when Phase 1 begins.

**Recommended action:** run a Phase 0.5 documentation reconciliation pass. Do not write production application code until that pass is complete and reviewed.

## What is already strong

The following areas are well represented and should remain architectural anchors:

- Dataset-agnostic core and explicit benchmark isolation.
- SQLite control/knowledge plane separated from Parquet/file analytical plane.
- Structured-data-only V1.0 scope.
- Multi-table relationship and join-safety design.
- Sampling provenance and the 500-row random-sample distinction.
- Semantic object model, conflict workflow, feature lineage, measurement units, prediction horizon.
- KPI/metric dependency graph and qualified measures.
- Four-gate capability discovery.
- Baseline-first modelling and leakage checks.
- Predictive, deterministic, benchmark, Monte Carlo, and SDV simulation boundaries.
- Trust Engine as an independent gate.
- ML-only/local/remote/hybrid LLM architecture.
- Sensitive/quasi-identifier and remote-transmission policy.
- Job abstraction and local-worker-first architecture.
- Persisted Run Result Object and reproducible simulation history.
- Anti-causal-language and anti-benchmark-contamination principles.
- Canonical HTML design system and complete dark/light V1.0 requirement.

## Document classification

### PASS — no material correction required

These files are directionally consistent and may remain as the authority, aside from minor wording updates caused by cross-document reconciliation:

- `00_SCOPE_FREEZE.md`
- `01_PROJECT_SPEC.md`
- `02_PRODUCT_REQUIREMENTS.md`
- `03_ARCHITECTURE.md`
- `07_DATA_UNDERSTANDING_SPEC.md`
- `08_SEMANTIC_MODEL_SPEC.md`
- `09_RELATIONSHIPS_HIERARCHY_LINEAGE_SPEC.md`
- `10_KPI_METRIC_DEPENDENCY_SPEC.md`
- `11_CAPABILITY_DISCOVERY_SPEC.md`
- `12_MODELING_ENGINE_SPEC.md`
- `13_MODEL_REGISTRY_LIFECYCLE_SPEC.md`
- `14_SIMULATION_ENGINE_SPEC.md`
- `16_LLM_ARCHITECTURE.md`
- `17_PRIVACY_REMOTE_LLM_POLICY.md`
- `19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `20_INGESTION_STORAGE_SPEC.md`
- `21_SAMPLING_PROVENANCE_SPEC.md`
- `23_ERROR_HANDLING_SPEC.md`
- `25_REPORTING_EXPORT_SPEC.md`
- `26_SIMULATION_HISTORY_REPRODUCIBILITY.md`
- `28_REST_API_CONTRACT.md`
- `33_OPEN_QUESTIONS.md`
- `34_CODING_STANDARDS.md`
- `36_BACKUP_RETENTION_RECOVERY.md`
- `38_GLOSSARY.md`
- `39_BENCHMARK_CATALOG.md`
- `40_ANTI_CONTAMINATION.md`

### PASS WITH CLARIFICATION / SMALL UPDATE

- `04_PROJECT_STRUCTURE.md`
- `05_UI_UX_SPEC.md`
- `06_UI_DESIGN_SYSTEM.md`
- `15_TRUST_AND_VALIDATION_SPEC.md`
- `18_SECURITY_RBAC_SPEC.md`
- `22_OBSERVABILITY_AUDIT_SPEC.md`
- `24_JOB_PROCESSING_SPEC.md`
- `27_SQLITE_SCHEMA_SPEC.md`
- `29_TEST_STRATEGY.md`
- `30_ACCEPTANCE_CRITERIA.md`
- `31_IMPLEMENTATION_PROGRESS.md`
- `32_DECISION_LOG.md`
- `35_CONFIGURATION_SPEC.md`
- `37_SYSTEM_HEALTH_SPEC.md`

### REQUIRES MAJOR CORRECTION

- `PHASE_0_IMPLEMENTATION_PLAN.md`

---

# Cross-document findings

## F-001 — Authorization has two competing authorities

### Good specification
`18_SECURITY_RBAC_SPEC.md` defines Admin/User through role-to-permission mapping.

### Drift introduced by plan
`PHASE_0_IMPLEMENTATION_PLAN.md` adds persisted `User.is_admin`, exposes it in profile output, and uses it in fixtures.

### Required resolution
There must be one authorization authority:

`User -> Role -> RolePermission -> Permission`

For V1.0 a user may have one role if desired. `Admin` and `User` are role records, not Boolean authorization flags.

Do not persist or authorize from an independent `is_admin` field.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `18_SECURITY_RBAC_SPEC.md` to explicitly state the authority
- `27_SQLITE_SCHEMA_SPEC.md` to show the user-role relation
- `29_TEST_STRATEGY.md`
- `30_ACCEPTANCE_CRITERIA.md`

---

## F-002 — ORM and API-schema ownership is inconsistent

The plan describes `auth/models.py` as Pydantic models but then defines SQLAlchemy entities there, while also defining database models elsewhere.

### Required resolution
Use one ORM definition per table.

Recommended pattern:

- `backend/ipsp/database/models/...` — SQLAlchemy ORM
- `backend/ipsp/api/schemas/...` or domain `schemas.py` — Pydantic request/response/contracts
- `backend/ipsp/auth/...` — auth services/policies/domain logic

No duplicate ORM entity definitions.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `04_PROJECT_STRUCTURE.md`
- `34_CODING_STANDARDS.md`

---

## F-003 — Synchronous and asynchronous database patterns are mixed

The plan uses synchronous SQLAlchemy `Session` and legacy `Session.query()` inside `async def` repository/service methods.

### Required resolution
For V1.0 foundation use a coherent synchronous SQLAlchemy 2.x control-plane pattern unless a deliberate Decision Log entry selects fully asynchronous SQLAlchemy.

Recommended:
- synchronous SQLAlchemy Session
- SQLAlchemy 2.x `select()` / `Session.execute()` / `Session.scalars()`
- synchronous repository/service methods for SQLite metadata work
- background jobs for profiling/training/simulation/report work

Do not create fake async around blocking synchronous database operations.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `34_CODING_STANDARDS.md`
- `32_DECISION_LOG.md` if this choice is formally locked

---

## F-004 — Generated dependency pins are stale and should not become implementation authority

The Phase 0 plan contains old exact pins and unnecessary packages.

### Required resolution
- Re-resolve maintained compatible dependencies when Phase 1 begins.
- Declare direct dependencies in `pyproject.toml`.
- Add a reproducible lock/constraints process.
- Do not list `sqlite3` as a pip package.
- Prefer `pwdlib[argon2]` for new Argon2id password hashes.
- Do not introduce JWT/python-jose merely for browser login; V1.0 uses server-side sessions.
- Do not add bcrypt as a new-password fallback unless a legacy-hash migration requirement exists.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `35_CONFIGURATION_SPEC.md` only if dependency/version policy is documented there
- `29_TEST_STRATEGY.md` if dependency/security regression checks are added

---

## F-005 — Session lifecycle/security needs a stronger contract

The security spec is directionally correct but the plan treats cookie flags as session-fixation mitigation.

### Required resolution
- cryptographically random opaque session token
- new token after successful authentication
- rotation/invalidation after password or privilege/role changes
- explicit expiration and logout invalidation
- raw session token never logged
- preferably store only a hash of the session bearer token
- HttpOnly
- Secure under HTTPS/production with explicit localhost development behavior
- suitable SameSite policy
- CSRF on browser state-changing operations
- failed-login throttling/temporary lockout
- timezone-aware UTC timestamps

Update:
- `18_SECURITY_RBAC_SPEC.md`
- `22_OBSERVABILITY_AUDIT_SPEC.md`
- `27_SQLITE_SCHEMA_SPEC.md`
- `29_TEST_STRATEGY.md`
- `30_ACCEPTANCE_CRITERIA.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`

---

## F-006 — Audit envelope should not contain raw `session_id`

`22_OBSERVABILITY_AUDIT_SPEC.md` includes `session_id` in the common event envelope while correctly banning raw cookies and secrets.

### Required resolution
Rename to a safe correlation field such as:

`session_correlation_id`

and define it as non-secret / hashed / pseudonymous. Never log the bearer session token itself.

Also keep high-volume application/runtime logs outside SQLite; persist durable audit/security events in SQLite when needed.

Update:
- `22_OBSERVABILITY_AUDIT_SPEC.md`
- `27_SQLITE_SCHEMA_SPEC.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`

---

## F-007 — Production secret behavior is unsafe in the plan

The plan proposes generating a new random `secret_key` as a default on startup.

### Required resolution
- Required production secrets fail closed when missing.
- Stable secrets come from SecretProvider/environment/protected OS storage.
- Development-only secret bootstrap is explicit.
- No ordinary plaintext provider secrets in SQLite.
- Pepper is optional and, if enabled, stable and external to the password database.

Update:
- `19_OUTBOUND_SECRETS_CONFIG_SPEC.md`
- `35_CONFIGURATION_SPEC.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `30_ACCEPTANCE_CRITERIA.md`

---

## F-008 — CDN usage conflicts with local-first/offline design

The plan says `Plotly.js latest CDN`.

This conflicts with local-first operation and introduces uncontrolled dependency drift.

### Required resolution
- explicitly select a Plotly.js version
- vendor the production asset under `frontend/assets/vendor/`
- store license/version metadata
- runtime must not require public CDN access
- future external asset access must obey OutboundPolicy

Update:
- `05_UI_UX_SPEC.md`
- `06_UI_DESIGN_SYSTEM.md`
- `30_ACCEPTANCE_CRITERIA.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`

---

## F-009 — Dark/light theme requirement is correct, but implementation sequencing is inconsistent

`05_UI_UX_SPEC.md`, `06_UI_DESIGN_SYSTEM.md`, and `30_ACCEPTANCE_CRITERIA.md` require both themes.

The plan marks light theme as a Phase 7 placeholder and `31_IMPLEMENTATION_PROGRESS.md` groups light theme with v0.7 dynamic frontend.

### Required resolution
Foundation phase must create:
- shared semantic design tokens
- dark theme tokens
- light theme tokens
- theme switch/persistence architecture

Full page implementation may still mature at v0.7.0.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `31_IMPLEMENTATION_PROGRESS.md`
- optionally clarify `06_UI_DESIGN_SYSTEM.md`

---

## F-010 — Dataset versioning is correctly specified in SQLite spec but weakened in plan

`27_SQLITE_SCHEMA_SPEC.md` already contains `datasets` and `dataset_versions` and states that referenced versions are immutable.

The plan later talks about a mutable `Dataset.version`.

### Required resolution
Use logical identity + immutable version records.

At minimum:
- datasets
- dataset_versions
- semantic manifest/version rows
- model version/artifact rows
- simulation_runs referencing exact immutable records
- capability version/reference
- seed/config snapshot/hash

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `27_SQLITE_SCHEMA_SPEC.md` to make exact references explicit
- `26_SIMULATION_HISTORY_REPRODUCIBILITY.md`
- `30_ACCEPTANCE_CRITERIA.md`

---

## F-011 — Redundant `is_multi_table` state should be removed

The plan proposes a Boolean `is_multi_table` even though the architecture already has `dataset_tables`.

### Required resolution
Derive multi-table state from table count. Do not create mutable duplicate truth.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- optionally state this explicitly in `27_SQLITE_SCHEMA_SPEC.md`

---

## F-012 — Migration ownership is inconsistent

`04_PROJECT_STRUCTURE.md` shows the canonical root:

`database/{migrations,sql}/`

The plan additionally proposes package-local Alembic migration history.

### Required resolution
Choose one migration root and one Alembic history. Recommended: retain the repository-root `database/migrations/` structure already in the architecture pack.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `04_PROJECT_STRUCTURE.md` only if more explicit wording is useful

---

## F-013 — Auth route ownership is duplicated in the plan

The plan contains both an auth package router and an API auth module.

### Required resolution
One canonical API route location, e.g.:

`backend/ipsp/api/routes/auth.py`

Auth package owns:
- service
- schemas/domain policy where appropriate
- password/session helpers

Routes stay thin.

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `04_PROJECT_STRUCTURE.md`

---

## F-014 — Sampling provenance rule needs one nuance

`21_SAMPLING_PROVENANCE_SPEC.md` is good.

The plan phrase that capability gates should ignore sample size alone can be misread.

### Required resolution
A 500-row sample must not be treated as proof that the full source dataset has only 500 rows or the same rare-category counts.

But if a model is actually trained on that 500-row sample, the sample size absolutely matters to the statistical validation of that model.

Keep the lifecycle:
`DISCOVERED -> VALIDATING -> VALIDATED -> ENABLED`

Update:
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `21_SAMPLING_PROVENANCE_SPEC.md` only if desired for extra clarity

---

## F-015 — Negative financial values need neutral treatment

The Trust spec correctly rejects a universal `revenue >= 0` rule but says a valid negative may be a business exception.

### Required resolution
A negative value is:
- invalid only when mathematically impossible or contradictory to a confirmed semantic/business rule;
- an anomaly only when evidence supports unusualness;
- otherwise a valid observed value.

Do not automatically classify it as an exception.

Update:
- `15_TRUST_AND_VALIDATION_SPEC.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`

---

## F-016 — Job abstraction exists in docs but is missing from Phase 1 foundation blueprint

`24_JOB_PROCESSING_SPEC.md` correctly defines a local worker + SQLite-backed job metadata and `JobBackend` abstraction.

### Required resolution
Phase 1 foundation must create contracts/types/repository schema needed for jobs even if full execution comes later.

Suggested interfaces:
- JobService
- JobBackend
- JobRepository
- JobStatus
- JobType
- progress/cancel/retry/error contract

Do not introduce Redis/Celery as required dependencies.

Update:
- `24_JOB_PROCESSING_SPEC.md`
- `27_SQLITE_SCHEMA_SPEC.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `31_IMPLEMENTATION_PROGRESS.md`

---

## F-017 — Health design should distinguish liveness/readiness/admin diagnostics

`37_SYSTEM_HEALTH_SPEC.md` describes the rich Admin health page but the implementation plan only shows one generic `/health`.

### Required resolution
Separate:
- liveness — process alive
- readiness — DB/storage/required runtime dependencies ready
- Admin system health — detailed diagnostics

No bare `except:`. Client responses stay safe.

Update:
- `37_SYSTEM_HEALTH_SPEC.md`
- `28_REST_API_CONTRACT.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`
- `29_TEST_STRATEGY.md`

---

## F-018 — User schema should follow username/password requirement

`02_PRODUCT_REQUIREMENTS.md` says local username/password authentication.

The plan makes email mandatory.

### Required resolution
Email should be optional unless another feature later requires it.

Recommended user fields:
- id
- username
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

No persisted independent `is_admin`.

Update:
- `18_SECURITY_RBAC_SPEC.md`
- `27_SQLITE_SCHEMA_SPEC.md`
- `PHASE_0_IMPLEMENTATION_PLAN.md`

---

## F-019 — Implementation progress currently authorizes Phase 1 too early

`31_IMPLEMENTATION_PROGRESS.md` currently says Phase 1 is ready to begin.

After this audit, that statement is no longer valid.

### Required resolution
Add a Phase 0.5 milestone:

`Architecture correction + documentation reconciliation`

Set:
- Phase 0 = plan generated
- Phase 0.5 = IN REVIEW / NOT COMPLETE
- Phase 1 = BLOCKED pending Phase 0.5 PASS

Update:
- `31_IMPLEMENTATION_PROGRESS.md`

---

# Additional completeness improvements

These are not architectural blockers but should be incorporated during Phase 0.5.

## A-001 — Add local vendor asset policy
Extend UI/design docs with `frontend/assets/vendor/` policy, version/license inventory, and no runtime CDN requirement.

## A-002 — Add dependency management policy
`pyproject.toml` is the source of direct dependencies; use a lock/constraints mechanism for reproducibility. Avoid exact package lists in architecture docs becoming permanently stale.

## A-003 — Add user/role relationship to schema documentation
The current SQLite table-group list should explicitly state whether V1.0 uses `users.role_id` or a `user_roles` join table. Since only Admin/User are required, a single role per user is acceptable and simpler.

## A-004 — Add session table semantics
Document hashed token lookup, expiry, invalidation, created/last-seen timestamps, user agent/IP metadata only if privacy policy approves, and never storing/logging raw bearer tokens.

## A-005 — Add immutable configuration snapshot for simulation runs
Persist or hash the effective runtime configuration relevant to numerical reproducibility without copying secrets.

---

# Phase 0.5 pass criteria

Phase 1 may begin only after all are true:

1. `PHASE_0_IMPLEMENTATION_PLAN.md` is corrected.
2. `is_admin` is eliminated as an authorization source.
3. ORM vs Pydantic ownership is unambiguous.
4. One SQLAlchemy execution model is selected.
5. One Alembic migration location exists.
6. One API route ownership structure exists.
7. Server-side session lifecycle is fully specified.
8. Production secrets fail closed rather than regenerate silently.
9. Runtime CDN dependencies are prohibited.
10. Dark + light theme foundation is scheduled in v0.1.0.
11. Dataset/version/semantic/model/run references are immutable/reproducible.
12. `is_multi_table` duplicate state is removed.
13. Audit envelope uses a safe session correlation identifier.
14. Job contracts are present in the foundation.
15. Liveness/readiness/admin-health are separated.
16. User email is optional unless explicitly required.
17. Sampling semantics distinguish source population from the dataset actually trained.
18. No universal negative-finance rule exists.
19. Documentation consistency scan reports no contradictory implementation guidance.
20. `31_IMPLEMENTATION_PROGRESS.md` marks Phase 0.5 PASS and only then unblocks Phase 1.

## Final conclusion

The IPSP V1.0 architecture is **ready to be frozen after a correction pass, not redesigned**.

The numbered specifications are generally strong. The generated Phase 0 implementation plan is the main source of drift.

**Phase 1 status: BLOCKED pending Phase 0.5 reconciliation.**
