# IPSP Phase 0.5 — Documentation Reconciliation Report

**Report date:** 2026-08-11  
**Audit status:** COMPLETE  
**Correction execution status:** COMPLETE  
**Phase 0.5 gate:** PASS

## Executive result

The approved IPSP v1.0 architecture was retained. The implementation-plan drift identified by the Phase 0 audit was corrected directly in the authoritative specifications and `PHASE_0_IMPLEMENTATION_PLAN.md`. No production code was created.

The original audit count is normalized here as **19 cross-document findings (F-001–F-019) plus 5 completeness improvements (A-001–A-005), for 24 total items**. This resolves the earlier report's mismatch between a claimed total of 24 and detailed numbering ending at 22.

## Resolution register

| ID | Result | Files modified | Exact resolution and verification |
|---|---|---|---|
| F-001 Authorization authority | RESOLVED | `18_SECURITY_RBAC_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, `29_TEST_STRATEGY.md`, `30_ACCEPTANCE_CRITERIA.md`, `32_DECISION_LOG.md`, plan | Locked `User.role_id → Role → RolePermission → Permission` as sole authority; removed persisted/admin-Boolean examples. Scan found no persisted or authorizing admin Boolean in corrected architecture. |
| F-002 ORM/API ownership | RESOLVED | `04_PROJECT_STRUCTURE.md`, `32_DECISION_LOG.md`, `34_CODING_STANDARDS.md`, plan | ORM entities now have one canonical `database/models/` home; Pydantic API contracts use `api/schemas/`. Presence scan found both canonical locations; duplicate examples were removed. |
| F-003 DB execution model | RESOLVED | `27_SQLITE_SCHEMA_SPEC.md`, `32_DECISION_LOG.md`, `34_CODING_STANDARDS.md`, plan | Locked synchronous SQLAlchemy 2.x with `select()`/`execute()`/`scalars()` and jobs for heavy work. Scan found zero mixed synchronous-Session/async repository guidance and zero legacy query use outside explicit prohibitions. |
| F-004 Dependency policy | RESOLVED | `35_CONFIGURATION_SPEC.md`, plan | Removed stale exact pins; direct dependencies belong in `pyproject.toml` with lock/constraints resolution at implementation time. Exact-pin scan returned zero architecture matches. |
| F-005 Session lifecycle | RESOLVED | `18_SECURITY_RBAC_SPEC.md`, `22_OBSERVABILITY_AUDIT_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, `29_TEST_STRATEGY.md`, `30_ACCEPTANCE_CRITERIA.md`, `32_DECISION_LOG.md`, plan | Added opaque token rotation, hash-only storage, expiry/logout/password/role invalidation, throttling/lockout, cookie/CSRF rules, UTC timestamps, and raw-token prohibition. Presence scan found seven rotation references and seven safe-correlation references. |
| F-006 Audit session identifier | RESOLVED | `22_OBSERVABILITY_AUDIT_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, `30_ACCEPTANCE_CRITERIA.md`, plan | Event envelope now uses non-secret `session_correlation_id`; raw bearer values are prohibited. Raw-session-log contradiction scan returned zero. |
| F-007 Production secrets | RESOLVED | `19_OUTBOUND_SECRETS_CONFIG_SPEC.md`, `30_ACCEPTANCE_CRITERIA.md`, `32_DECISION_LOG.md`, `35_CONFIGURATION_SPEC.md`, plan | Required production secrets are stable and fail closed; development bootstrap is explicit. Generated-secret-default scan returned zero. |
| F-008 Offline frontend | RESOLVED | `05_UI_UX_SPEC.md`, `06_UI_DESIGN_SYSTEM.md`, `30_ACCEPTANCE_CRITERIA.md`, `32_DECISION_LOG.md`, plan | Browser bundles are pinned, vendored under `frontend/assets/vendor/`, and inventoried for version/license. Runtime-CDN scan returned zero. |
| F-009 Theme sequencing | RESOLVED | `05_UI_UX_SPEC.md`, `06_UI_DESIGN_SYSTEM.md`, `30_ACCEPTANCE_CRITERIA.md`, `32_DECISION_LOG.md`, plan | v0.1.0 now owns shared tokens, dark/light token sets, switching, and persistence; v0.7.0 applies the foundation to full pages. Deferred-theme scan returned zero. |
| F-010 Immutable versioning | RESOLVED | `26_SIMULATION_HISTORY_REPRODUCIBILITY.md`, `27_SQLITE_SCHEMA_SPEC.md`, `30_ACCEPTANCE_CRITERIA.md`, plan | Logical datasets and immutable dataset/semantic/capability/model versions are explicit; runs reference exact records and persist seed plus non-secret configuration snapshot/hash. Presence scan found nine immutable-reference matches. |
| F-011 Multi-table truth | RESOLVED | `27_SQLITE_SCHEMA_SPEC.md`, plan | Multi-table status derives from `dataset_tables`; no duplicate Boolean is persisted. Persisted-state scan returned zero contradictions; remaining term usage is prohibitive documentation only. |
| F-012 Migration ownership | RESOLVED | `04_PROJECT_STRUCTURE.md`, `27_SQLITE_SCHEMA_SPEC.md`, `32_DECISION_LOG.md`, `34_CODING_STANDARDS.md`, plan | `database/migrations/` is the sole Alembic root. Package-local migration-root scan returned zero. |
| F-013 Route ownership | RESOLVED | `04_PROJECT_STRUCTURE.md`, `28_REST_API_CONTRACT.md`, `32_DECISION_LOG.md`, `34_CODING_STANDARDS.md`, plan | Thin FastAPI routes live only under `backend/ipsp/api/routes/`; domain packages own services/policies. Duplicate auth-router scan returned zero. |
| F-014 Sampling nuance | RESOLVED | `21_SAMPLING_PROVENANCE_SPEC.md`, plan | Source-population inference is separated from the actual model training sample size; lifecycle remains DISCOVERED through ENABLED. Presence scan found two explicit training-size statements. |
| F-015 Negative finance values | RESOLVED | `15_TRUST_AND_VALIDATION_SPEC.md`, plan | Negative values are invalid only under intrinsic/confirmed rules, anomalous only with evidence, and otherwise valid. Universal-rule scan found only explicit prohibitions, not affirmative rules. |
| F-016 Job foundation | RESOLVED | `24_JOB_PROCESSING_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, `29_TEST_STRATEGY.md`, `30_ACCEPTANCE_CRITERIA.md`, plan | Added `JobBackend`, `JobService`, `JobRepository`, `JobStatus`, `JobType`, progress/cancel/retry/error contracts and schema to v0.1.0. Redis/Celery remain optional future implementations. |
| F-017 Health tiers | RESOLVED | `28_REST_API_CONTRACT.md`, `29_TEST_STRATEGY.md`, `30_ACCEPTANCE_CRITERIA.md`, `37_SYSTEM_HEALTH_SPEC.md`, plan | Separated liveness, readiness, and authorized Admin diagnostics; prohibited bare exception handling/raw diagnostics. Presence scan confirmed all tiers. |
| F-018 User schema | RESOLVED | `18_SECURITY_RBAC_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, plan | Added the required user fields, nullable email, single `role_id`, and timezone-aware UTC semantics. Independent admin Boolean removed. |
| F-019 Progress gate | RESOLVED | `31_IMPLEMENTATION_PROGRESS.md`, plan, this report | Phase 0.5 is marked PASS only after corrections and verification; Phase 1 is set READY afterward. Premature-readiness scan before sign-off returned zero. |
| A-001 Vendor asset policy | RESOLVED | `05_UI_UX_SPEC.md`, `06_UI_DESIGN_SYSTEM.md`, `30_ACCEPTANCE_CRITERIA.md`, plan | Added local vendor path and version/license inventory. |
| A-002 Dependency management | RESOLVED | `35_CONFIGURATION_SPEC.md`, plan | Added maintained-version resolution plus direct-dependency and reproducible lock/constraints policy. |
| A-003 User-role relationship | RESOLVED | `18_SECURITY_RBAC_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, `32_DECISION_LOG.md`, plan | Explicitly locked one `role_id` per V1.0 user and role-permission authorization. |
| A-004 Session table semantics | RESOLVED | `18_SECURITY_RBAC_SPEC.md`, `22_OBSERVABILITY_AUDIT_SPEC.md`, `27_SQLITE_SCHEMA_SPEC.md`, plan | Added token hash, correlation ID, lifecycle timestamps, expiry/invalidation and no raw token storage/logging. |
| A-005 Run configuration snapshot | RESOLVED | `26_SIMULATION_HISTORY_REPRODUCIBILITY.md`, `27_SQLITE_SCHEMA_SPEC.md`, `30_ACCEPTANCE_CRITERIA.md`, plan | Added effective non-secret configuration snapshot/hash to exact run reproducibility. |

## Verification evidence

The corrected-architecture scan covered `AGENTS.md`, `.github/copilot-instructions.md`, numbered specifications `00`–`40`, and `PHASE_0_IMPLEMENTATION_PLAN.md`.

Contradiction searches returned zero actionable matches for:

- mixed synchronous Session work in async repositories/services;
- stale exact dependency pins or `sqlite3` package guidance;
- runtime CDN guidance;
- generated production-secret defaults;
- package-local migration roots or duplicate auth route locations;
- raw session identifiers in log/audit envelopes;
- deferred-only light-theme foundation;
- premature Phase 1 readiness.

Lexical searches for `is_admin`, `Session.query`, `is_multi_table`, Redis/Celery, and `revenue >= 0` matched only explicit prohibition/optional-policy sentences in corrected specifications. Manual review found zero affirmative contradictory guidance.

Required-contract presence checks all passed: role-permission authority (2 matches), canonical ORM home (8), API schema home (2), synchronous SQLAlchemy 2.x (5), single migration root (6), single route home (7), session rotation (7), session correlation (7), fail-closed secrets (6), vendored assets (4), early dark/light foundation (4), immutable references (9), job foundation (1), health separation (3), training-sample nuance (2), and negative-value neutrality (2).

The benchmark-contamination scan found benchmark terms only in anti-contamination rules, violation checks, and the canonical-UI disclaimer. No benchmark-specific production architecture or behavior was introduced.

## Phase 0.5 completion gate

1. ✅ Independent admin authorization removed.
2. ✅ Canonical ORM ownership established.
3. ✅ Duplicate ORM guidance removed.
4. ✅ Synchronous SQLAlchemy 2.x execution locked.
5. ✅ Fake async database guidance removed.
6. ✅ Legacy query guidance removed.
7. ✅ Single Alembic root established.
8. ✅ Single API route location established.
9. ✅ Complete session lifecycle specified.
10. ✅ Raw session tokens excluded from logs; safe correlation specified.
11. ✅ Production secrets fail closed.
12. ✅ Runtime CDN dependencies prohibited.
13. ✅ Dark/light foundation moved to v0.1.0.
14. ✅ Immutable version/run references specified.
15. ✅ Duplicate multi-table state removed.
16. ✅ Audit envelope corrected.
17. ✅ Job contracts/schema included in foundation.
18. ✅ Health tiers separated.
19. ✅ Consistency and contamination scans passed after manual classification of prohibition-only matches.
20. ✅ Progress updated only after gates 1–19 passed.

## Unresolved issues

None. The non-blocking choices in `33_OPEN_QUESTIONS.md` remain non-blocking and unchanged.

## Final Micro-Cleanup

- **R-001 — RESOLVED:** Normalized implementation and test terminology in `PHASE_0_IMPLEMENTATION_PLAN.md` to `Phase 1 / v0.1.0`; Phase 0 remains the planning phase and Phase 0.5 the documentation-reconciliation phase.
- **R-002 — RESOLVED:** Replaced the obsolete fixed SQLite table list with the control/knowledge/governance-plane rule and retained file/Parquet storage for raw analytical rows.
- **R-003 — RESOLVED:** Clarified that application/Admin APIs use `/api/v1`, infrastructure probes `/health/live` and `/health/ready` are intentionally unversioned, and rich diagnostics use `/api/v1/admin/system/health`.
- **R-004 — RESOLVED:** RBAC/authentication services now raise typed IPSP/domain exceptions; centralized FastAPI handling owns HTTP mapping and the safe error envelope.
- **R-005 — RESOLVED:** Plan examples now use subsystem-prefixed stable codes (`AUTH-*`, `AUTHZ-*`, `DATA-*`, and `SYS-*` as applicable) consistent with `23_ERROR_HANDLING_SPEC.md`.

Targeted verification found no residual implementation-oriented `Phase 0 Pass Criteria` or `Phase 0.1.0` wording, obsolete SQLite-only list, RBAC-raised `HTTPException`, ad-hoc authentication route mapping, or unprefixed example codes. Documentation Freeze remains PASS and Phase 1 remains READY.

## Final status

**Phase 0.5: PASS**  
**Phase 1: READY**
