# System Architecture

## High-level

```text
HTML/CSS/JS
    │
    ▼
FastAPI + Authentication/RBAC
    │
    ├── Application Services
    └── Job Manager/Worker
            │
            ▼
Data Understanding → Semantic Engine → Capability Discovery
       → Model Engine → Simulation Engine → Explainability
            │
            ▼
      Trust & Validation
            │
            ▼
 Results / History / PDF / Excel
```

## Cross-cutting services

- Authorization and dataset/column policy
- Dataset/version lineage
- Outbound access policy
- SecretProvider
- Configuration and feature flags
- Observability and trace propagation
- Error taxonomy
- Background jobs

## Storage planes

### Control/knowledge plane — SQLite
Users, permissions, projects, dataset metadata, semantic manifests, confirmations, capabilities, model registry, runs, jobs, provider configuration references, audit events.

### Analytical data plane — files/Parquet
Original uploads, canonicalized datasets, processed analytical views, model training data references, optional simulation samples.

## Portability
Use repository/provider abstractions so future PostgreSQL, object storage, distributed workers, and alternate LLM providers do not require redesign of the domain core.
