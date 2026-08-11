# V1.0 Acceptance Criteria

IPSP v1.0 is ready only when all critical criteria pass.

## Governance
- Admin/User login and permissions enforced server-side.
- Role-to-permission mapping is the sole authorization authority; no persisted admin Boolean is used.
- Dataset permissions work.
- Passwords securely hashed.
- Session tokens rotate on login, expire, invalidate on logout/password/role changes, are not logged raw, and state-changing browser requests enforce CSRF.
- Failed logins are throttled/temporarily locked and required production secrets fail closed.
- Remote/internet policy blocks disallowed calls.
- Secrets are not stored/logged in plaintext.

## Data
- All supported structured formats ingest safely.
- Multi-sheet/multi-table metadata supported.
- Candidate grain, roles, relationships, hierarchies, lineage, sampling provenance produced.
- Unsafe joins are detected.
- Semantic conflicts produce questions instead of silent assumptions.

## Capability
- Unsupported capabilities are visibly disabled with reasons.
- At least one regression/classification/forecast or other predictive path can be validated on suitable data.
- Deterministic what-if works without ML where formula semantics are confirmed.
- Similarity/look-alike path is available only when appropriate.

## Trust
- Predictive models beat or meaningfully justify themselves over baselines before enablement.
- Leakage checks run.
- Constraint classes are respected.
- P10/P50/P90 ordering and coverage checks exist where uncertainty is shown.
- Causal language is blocked/downgraded without causal support.

## UI
- Entire app follows canonical supplied design language.
- Dark and light themes complete.
- Shared dark/light tokens, switching, and preference persistence exist in the v0.1.0 foundation.
- Browser dependencies are pinned and vendored; production has no public-CDN runtime dependency.
- Dataset/simulation five-step flows function.
- Dynamic controls and results are metadata-driven.

## Operations
- Trace IDs propagate.
- Audit events use a non-secret `session_correlation_id` and high-volume runtime logs use an appropriate structured sink.
- Foundation job interfaces/schema cover status, progress, cancellation, retry, and safe errors without requiring Redis/Celery.
- Liveness, readiness, and authorized Admin diagnostics are separate and safe.
- Audit/security/ML/LLM/simulation/export errors are logged safely.
- Run history supports re-run/reproduce.
- Completed runs reference exact immutable dataset/semantic/capability/model versions, seed, and effective non-secret configuration snapshot/hash.
- PDF and Excel export from persisted Run Result Object.
- Basic health and backup/restore are functional.
