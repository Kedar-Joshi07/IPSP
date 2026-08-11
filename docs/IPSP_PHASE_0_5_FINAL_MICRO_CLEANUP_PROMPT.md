# Codex Prompt — Phase 0.5 Final Micro-Cleanup

You are working in the IPSP v1.0 repository.

The major Phase 0.5 reconciliation has passed. This is a **small final documentation-only cleanup** before Phase 1 production code begins.

## Absolute rules

- Do NOT write production Python, HTML, CSS, JavaScript, SQL migrations, or application code.
- Do NOT redesign IPSP.
- Do NOT perform another broad audit.
- Apply only the five residual documentation corrections below.
- Preserve all previously reconciled architecture decisions.
- After editing, run targeted searches and show the changed-file diff/stat.

## Read first

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `docs/23_ERROR_HANDLING_SPEC.md`
- `docs/27_SQLITE_SCHEMA_SPEC.md`
- `docs/28_REST_API_CONTRACT.md`
- `docs/31_IMPLEMENTATION_PROGRESS.md`
- `docs/32_DECISION_LOG.md`
- `docs/34_CODING_STANDARDS.md`
- `docs/PHASE_0_IMPLEMENTATION_PLAN.md`
- `docs/IPSP_PHASE_0_5_FINAL_GATE_REVIEW.md`

## Apply exactly these residual corrections

### R-001 — Normalize phase/version terminology in `PHASE_0_IMPLEMENTATION_PLAN.md`

The document correctly says Phase 0 produced planning/specification only and Phase 0.5 performed documentation reconciliation.

Therefore implementation/test requirements must not be labelled as Phase 0.

Change, as appropriate:

- `Dependency Policy (Phase 0.1.0)` -> `Dependency Policy (Phase 1 / v0.1.0)`
- `Phase 0.1.0 Minimum Viable Foundation` -> `Phase 1 / v0.1.0 Minimum Viable Foundation`
- `Violation Checklist for Phase 0` -> `Phase 1 / v0.1.0 Implementation Conformance Checklist`
- every implementation-oriented `Phase 0 Pass Criteria` -> `Phase 1 / v0.1.0 Pass Criteria`
- `Testing Strategy for Phase 0` -> `Testing Strategy for Phase 1 / v0.1.0`
- `Success Criteria for Phase 0` -> `Planned Success Criteria for Phase 1 / v0.1.0`
- `All Phase 0.1.0 tests pass` -> `All Phase 1 / v0.1.0 tests pass`
- any nearby wording that incorrectly implies production code/tests existed during Phase 0.

Do not rename the document itself; it remains the plan produced in Phase 0 and corrected in Phase 0.5.

### R-002 — Correct the SQLite control-plane checklist

In `PHASE_0_IMPLEMENTATION_PLAN.md`, remove the incorrect statement that SQLite holds only a short fixed list of tables.

Replace it with the architectural rule:

- SQLite stores control/knowledge/governance metadata only.
- This includes, as applicable, auth/RBAC, projects, dataset/version metadata, semantic metadata, capability/model registry metadata, simulation/run metadata, jobs, configuration references, user preferences, durable audit/security records, notifications/backups and other control-plane state defined by `27_SQLITE_SCHEMA_SPEC.md`.
- Raw analytical dataset rows remain outside SQLite in the file/Parquet analytical data plane.

Do not duplicate the entire SQLite schema in the checklist. `27_SQLITE_SCHEMA_SPEC.md` remains authoritative for exact table groups.

### R-003 — Clarify health route versioning

Update `28_REST_API_CONTRACT.md` and any affected implementation-plan example so there is no ambiguity:

- business/application/admin REST APIs use `/api/v1`;
- `/health/live` and `/health/ready` are intentionally unversioned infrastructure probe endpoints;
- `/api/v1/admin/system/health` is the versioned, authorized rich diagnostic endpoint.

### R-004 — Keep HTTP exceptions out of RBAC/domain services

In `PHASE_0_IMPLEMENTATION_PLAN.md`:

- `RBACService.enforce_permission()` must raise an IPSP/domain authorization exception such as `PermissionDeniedException`, not FastAPI `HTTPException`.
- Authentication/domain services raise typed IPSP/domain exceptions.
- Central FastAPI exception handling maps those exceptions to HTTP status codes and the stable safe error envelope.
- Routes remain thin.
- Remove ad-hoc route exception examples that contradict centralized error handling, or clearly show delegation to the shared exception layer.

Keep this consistent with `23_ERROR_HANDLING_SPEC.md` and `34_CODING_STANDARDS.md`.

### R-005 — Align example error codes with the error taxonomy

Update the implementation-plan error examples so they use or explicitly conform to subsystem-prefixed stable codes defined by `23_ERROR_HANDLING_SPEC.md`.

At minimum:
- authentication errors use `AUTH-*`;
- authorization errors use `AUTHZ-*`;
- other subsystem errors use their corresponding documented prefix.

Do not create a conflicting second taxonomy.

## Targeted verification

Before completion, verify:

1. `PHASE_0_IMPLEMENTATION_PLAN.md` contains no implementation/test pass criteria incorrectly labelled `Phase 0 Pass Criteria`.
2. No `Phase 0.1.0` wording remains where `v0.1.0` is intended.
3. No statement says SQLite holds only the obsolete six-table list.
4. `28_REST_API_CONTRACT.md` explicitly distinguishes unversioned probe routes from versioned application/admin routes.
5. `RBACService` does not raise FastAPI `HTTPException`.
6. Error examples conform to subsystem-prefixed taxonomy.
7. No production source code was created or modified.

## Progress/reporting

Do not reopen the major Phase 0.5 findings.

Update `docs/PHASE_0_5_RECONCILIATION_REPORT.md` with a short **Final Micro-Cleanup** section listing R-001 through R-005 as resolved.

`31_IMPLEMENTATION_PROGRESS.md` may continue to show Phase 0.5 PASS / Phase 1 READY after these corrections.

## Final response

Show:
- files modified;
- `git diff --stat`;
- targeted verification results;
- unresolved issues;
- `Documentation Freeze: PASS/FAIL`;
- `Phase 1: READY/BLOCKED`.

If all five corrections pass, report:

**Documentation Freeze: PASS**  
**Phase 1: READY**
