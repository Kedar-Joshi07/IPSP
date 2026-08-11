# Test Strategy

## Test layers

### Unit
Profilers, semantic rules, formula validation, relationship/cardinality analysis, trust checks, providers, permission helpers.

### Integration
Upload→profile→manifest, DB/repositories, model training/validation, simulation→trust→history, exports, LLM provider schema validation.

### Security
Auth, CSRF/session behavior, login token rotation, hashed-token storage, expiry/logout/password/role-change invalidation, failed-login throttling/lockout, role-to-permission-only authorization, dataset/column policy, remote-policy denial, fail-closed secrets, upload/path traversal, and secret/session-token log redaction.

### ML/model
Baselines, split strategy, leakage detection, calibration, reproducibility, model registry/promotion.

### Semantic benchmark
Known datasets assert expected *discovered concepts*, not benchmark-specific code paths.

### Acceptance/E2E
Admin bootstrap, dataset onboarding, clarification, capability discovery, run simulation, trust output, history, PDF/Excel.

### Architecture conformance
Verify one ORM definition per entity, separate Pydantic contracts, synchronous SQLAlchemy 2.x repository patterns, one migration history, one route location, vendored browser assets, both foundation themes, job contracts, immutable run references, and distinct liveness/readiness/Admin-health behavior.

## Benchmark principle
The full large RdF dataset is useful for scale. Several 500-row random samples are semantic/schema benchmarks. Do not use their row counts to reject full-dataset model capabilities.
