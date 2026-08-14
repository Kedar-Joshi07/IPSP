# Project Structure

## Status boundary

This document distinguishes the accepted repository structure from provider-neutral target
structure. Paths under **Current structure** exist in v0.1.0. Paths under **Planned conceptual
structure** are ownership guidance only and must not be described as implemented until created by an
accepted milestone.

## Current v0.1.0 structure

```text
IPSP/
├── frontend/
│   ├── assets/
│   ├── css/
│   └── js/
├── backend/ipsp/
│   ├── api/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── dependencies/
│   ├── auth/
│   ├── cli/
│   ├── config/
│   ├── database/models/
│   ├── errors/
│   ├── jobs/
│   ├── observability/
│   ├── repositories/
│   ├── security/
│   └── services/
├── database/migrations/
├── tests/
├── config/
├── docs/
├── flows/
├── prompts/
└── reference/
```

This tree is a responsibility summary rather than an exhaustive file listing.

## Planned conceptual structure

Later accepted milestones may add cohesive domain-neutral packages such as:

```text
backend/ipsp/
├── ingestion/
├── profiling/
├── semantics/
├── metrics/
├── domain_experiences/
├── cross_domain/
├── capabilities/
├── engines/
│   ├── ml/
│   ├── statistics/
│   ├── synthetic/
│   ├── optimization/
│   └── finance/
├── modelling/
├── scenarios/
├── simulation/
├── evidence/
├── trust/
├── learning/
├── llm/
├── explainability/
└── reports/
```

The tree expresses package boundaries, not required one-directory-per-concept implementation.
Milestone contract freezes decide exact module names and whether a package is needed. Domain
Experience Packs extend generic registries and services; they do not create separate product cores.

## Planned data and artifact organization

Provider-neutral conceptual targets are:

```text
data/
├── uploads/
├── staging/
├── quarantine/
└── processed/

artifacts/
├── models/
├── manifests/
├── reports/
├── simulations/
├── synthetic/
└── evidence/
```

No vendor receives a canonical artifact directory. Synthetic artifacts are organized by the generic
capability and retain provider, version, license, and provenance metadata rather than using a
provider-named target.

## Canonical ownership rules

- SQLAlchemy ORM entities are defined exactly once under `backend/ipsp/database/models/`.
- Pydantic API request/response schemas live under `backend/ipsp/api/schemas/`; domain packages may
  own non-API typed contracts but may not redefine ORM entities.
- FastAPI routes live only under `backend/ipsp/api/routes/`. Domain packages own services and
  policies, not duplicate routers.
- Repositories own SQLite/database access; SQL is not scattered through routes or services.
- `database/migrations/` is the single repository-wide Alembic history. Package-local migration
  roots are prohibited.
- Provider packages implement IPSP interfaces and do not become architecture authorities.
- Shared manifests, registries, graphs, evidence records, and learning contracts are versioned and
  owned by their frozen contract modules, not duplicated by Domain Experiences or providers.

## Growth rules

- Add a package only when an accepted milestone needs a cohesive ownership boundary.
- Do not create benchmark, dataset, customer, campaign, finance-field, or vendor-specific branches
  in generic core.
- Keep route modules thin, repositories explicit, services testable, and background execution behind
  JobBackend.
- Exact source-file counts are not contractual constraints.
- Future PostgreSQL, object storage, distributed workers, and alternate providers must remain
  possible through repositories and typed interfaces without redesigning core semantics.
