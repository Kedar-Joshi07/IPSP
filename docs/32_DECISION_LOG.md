# Architecture Decision Log

## Post-v0.1.0 F-002 authority

The [F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and
[Product Version and Development Roadmap Freeze](45_PRODUCT_VERSION_AND_DEVELOPMENT_ROADMAP_FREEZE.md)
govern architecture and sequencing decisions approved after formal acceptance of the v0.1.0
foundation. Where older target wording conflicts, F-002 wins. Existing D-001 through D-019 retain
their historical meanings; F-002 decisions use distinct `F002-Dxxx` identifiers and do not rewrite
accepted implementation history.

F-002 capabilities remain planned until their owning milestones are implemented, tested,
independently reviewed, and accepted.

## Locked decisions

### D-001 — Dataset-agnostic core
All benchmark/domain behavior is discovered from metadata/data or contained in optional domain extensions, never hardcoded into core.

### D-002 — Supplied HTML is canonical visual reference
Preserve design language; add full light theme. Hardcoded campaign content is prototype/demo content only.

### D-003 — FastAPI backend + HTML/CSS/vanilla JS frontend
No Streamlit. No framework migration unless a later decision explicitly changes it.

### D-004 — SQLite control plane + Parquet analytical plane
Do not force millions of analytical rows into SQLite.

### D-005 — Optional LLMs
ML-only must remain fully functional. Local/remote/hybrid providers share one contract.

### D-006 — Trust engine first-class
Every model/simulation/semantic proposal is independently validated.

### D-007 — Predictive vs causal separation
Observational association cannot be presented as causal effect.

### D-008 — Version everything required for reproducibility
Dataset, semantic manifest, model, scenario, seed/config.

### D-009 — Multi-table support in v1.0
Infer/propose/confirm relationships and validate join grain/cardinality.

### D-010 — Sampling provenance in v1.0
500-row random benchmark samples do not define full-population modelling limits.

### D-011 — Measurement-unit-aware journey graph
Ordered journey measures are not automatically strict monotonic funnels.

### D-012 — Sensitive-feature/remote-data governance
Column sensitivity and remote transmission policy are explicit.

### D-013 — No universal non-negative revenue rule
Only intrinsic/confirmed constraints can hard-block values.

### D-014 — Synchronous SQLAlchemy 2.x control plane
SQLite control-plane repositories and services are synchronous and use `select()`, `Session.execute()`, and `Session.scalars()`. Legacy `Session.query()` and synchronous Session work wrapped in `async def` are prohibited; heavy work runs through jobs.

### D-015 — Canonical ownership locations
SQLAlchemy ORM entities live only in `backend/ipsp/database/models/`, Pydantic API schemas in `backend/ipsp/api/schemas/`, routes in `backend/ipsp/api/routes/`, and the sole Alembic history in `database/migrations/`.

### D-016 — Role-to-permission authorization authority
V1.0 uses one `role_id` per user, and `User → Role → RolePermission → Permission` is the only authorization authority. No independent admin Boolean is persisted or checked.

### D-017 — Offline frontend and early theme foundation
Production browser assets are pinned and vendored locally. The v0.1.0 foundation includes shared dark/light tokens, switching, and preference persistence.

### D-018 — Secure opaque server sessions and fail-closed secrets
Browser authentication uses opaque server-side sessions with token rotation, hashed storage, lifecycle invalidation, expiry, CSRF protection, and no raw token logging. Required production secrets are stable and startup fails closed when they are absent.

### D-019 — Same-version parallel development with owner-controlled integration
Parallel implementation is organized as same-milestone, different-module workstreams behind explicit frozen contracts and path ownership. `main` contains accepted milestone states only. Feature branches merge through a milestone `integration/vX.Y.Z` branch. Kedar is the integration owner and final merge authority; contributors push only to assigned feature branches. Each milestone has one migration owner at a time, shared/integration-sensitive files require explicit ownership, and branch-level PASS does not replace post-merge integration and milestone acceptance gates.
