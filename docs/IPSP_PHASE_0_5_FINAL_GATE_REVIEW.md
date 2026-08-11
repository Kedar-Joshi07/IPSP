# IPSP v1.0 — Phase 0.5 Final Independent Gate Review

> **Post-review resolution (2026-08-11):** R-001 through R-005 were applied and verified by the final micro-cleanup recorded in `PHASE_0_5_RECONCILIATION_REPORT.md`. The review below is preserved as the pre-cleanup gate record; its conditional hold is satisfied. Documentation Freeze is PASS and Phase 1 is READY.

**Input reviewed:** latest revised `docs` archive after the Codex Phase 0.5 apply-corrections run.  
**Comparison basis:** prior revised archive from the previous Phase 0.5 attempt.  
**Review outcome:** **PASS WITH SMALL DOCUMENTATION CLEANUP REQUIRED BEFORE PHASE 1 CODE**

## Archive-change verification

The new archive contains 47 Markdown files.

Compared with the previous revised archive:
- 46 files are common.
- 23 existing Markdown files were substantively changed.
- 1 new Markdown file was added.
- 0 files were removed.

This is materially different from the earlier report-only run. The implementation plan itself was changed, along with the security, schema, UI, trust, jobs, API, test, configuration, health, decision-log and progress specifications.

## Major Phase 0.5 corrections independently verified

The latest docs now correctly establish:

- `User -> Role -> RolePermission -> Permission` as the sole authorization authority.
- No persisted `is_admin` authorization flag.
- One canonical SQLAlchemy ORM home: `backend/ipsp/database/models/`.
- Separate Pydantic API schemas: `backend/ipsp/api/schemas/`.
- One canonical FastAPI route location: `backend/ipsp/api/routes/`.
- One Alembic history: `database/migrations/`.
- Synchronous SQLAlchemy 2.x for the SQLite control plane.
- No affirmative legacy `Session.query()` guidance.
- Maintained dependency resolution at implementation time instead of stale hard pins.
- `sqlite3` treated as standard library.
- `pwdlib[argon2]` for new Argon2id hashes.
- Server-side opaque sessions rather than JWT browser login.
- Session rotation/hash-only storage/lifecycle invalidation and lockout/throttling requirements.
- Production secrets fail closed.
- Browser assets pinned and vendored locally; no runtime public CDN dependency.
- Shared dark and light theme foundation in v0.1.0.
- Logical dataset identity plus immutable version/reproducibility semantics.
- Multi-table state derived from `dataset_tables`.
- Safe `session_correlation_id` logging.
- Foundation job contracts without Redis/Celery as mandatory dependencies.
- Separate liveness/readiness/Admin diagnostic health concepts.
- Correct random-sample versus actual training-sample semantics.
- Neutral handling of negative financial values.
- Phase 0.5 marked PASS and Phase 1 marked READY only after the reconciliation pass.

## Residual cleanup findings

These are small, but they should be corrected before the first production-code prompt so Codex has only one interpretation.

### R-001 — Phase labels inside the implementation plan are still wrong

`PHASE_0_IMPLEMENTATION_PLAN.md` correctly states that Phase 0 wrote no production code, but later contains implementation/test requirements labelled as Phase 0, including:

- `Dependency Policy (Phase 0.1.0)`
- `Phase 0.1.0 Minimum Viable Foundation`
- `Violation Checklist for Phase 0`
- multiple `Phase 0 Pass Criteria`
- `Testing Strategy for Phase 0`
- `Success Criteria for Phase 0`
- `All Phase 0.1.0 tests pass`

Those requirements clearly belong to **Phase 1 / application version v0.1.0**.

**Required correction:** normalize those labels to `Phase 1 / v0.1.0` while keeping Phase 0 and Phase 0.5 documented as completed specification/reconciliation phases.

### R-002 — SQLite checklist contains an incorrect exhaustive table list

The implementation plan currently says:

> SQLite holds only `users`, `roles`, `permissions`, `sessions`, `audit_events`, `projects`.

This conflicts with the authoritative SQLite schema, which also includes role permissions, user sessions/preferences, dataset/version metadata, semantics, capabilities/models, simulation metadata, jobs, configuration references, notifications, backups, etc.

It also uses `sessions` whereas the schema uses `user_sessions`.

**Required correction:** replace the exhaustive list with a control-plane rule, e.g.:

> SQLite stores metadata/knowledge/governance/control-plane records (including auth/RBAC, projects, dataset/version metadata, semantics, capabilities/models, simulation metadata, jobs, configuration references and durable audit/security records). Raw analytical dataset rows remain outside SQLite in the analytical data plane.

### R-003 — Health route versioning should be explicit

`28_REST_API_CONTRACT.md` says `Use /api/v1` but also defines `/health/live` and `/health/ready` without the prefix.

This is a perfectly reasonable design for infrastructure probes, but it should be explicit.

**Required correction:** state that:
- business/application/admin API routes are versioned under `/api/v1`;
- `/health/live` and `/health/ready` are intentionally unversioned infrastructure probe endpoints;
- `/api/v1/admin/system/health` is the authorized rich diagnostic endpoint.

### R-004 — RBAC service example still leaks HTTP-layer concerns into the domain layer

The implementation plan's `RBACService.enforce_permission()` says it raises `HTTPException(403)`.

The project architecture otherwise says routes are thin and domain/services use the IPSP error taxonomy.

**Required correction:** `RBACService` should raise a domain/IPSP `PermissionDeniedException` (or equivalent). The FastAPI exception handler maps it to the stable HTTP 403 error envelope.

Similarly, authentication errors should flow through the centralized safe error mapping rather than requiring every route to construct ad-hoc HTTP error responses.

### R-005 — Error-code examples should align with the subsystem taxonomy

The implementation plan still shows generic codes such as:
- `VALIDATION_ERROR`
- `UNAUTHORIZED`
- `PERMISSION_DENIED`

The error specification defines subsystem-prefixed stable codes such as `AUTH-*`, `AUTHZ-*`, `DATA-*`, etc.

**Required correction:** update plan examples to use the canonical error-code taxonomy or explicitly delegate code construction to the central error layer.

## Gate decision

The Phase 0.5 execution itself was successful and Codex clearly applied the requested architecture corrections.

The remaining items are **documentation normalization/clarification**, not architecture redesign.

However, because the project is deliberately using documentation as implementation authority, these residual contradictions should be removed before production code begins.

**Phase 0.5 architectural outcome:** PASS  
**Documentation freeze:** PENDING MICRO-CLEANUP  
**Phase 1 production code:** HOLD until R-001 through R-005 are applied  
**Expected work:** one small documentation-only Codex run
