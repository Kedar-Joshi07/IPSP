# Target Project Structure

```text
ipsp/
├── frontend/
│   ├── *.html
│   ├── css/
│   ├── js/
│   └── assets/
├── backend/ipsp/
│   ├── api/
│   │   ├── routes/          # sole FastAPI route ownership; routers stay thin
│   │   └── schemas/         # Pydantic request/response contracts
│   ├── auth/
│   ├── security/
│   ├── database/
│   │   └── models/          # sole SQLAlchemy ORM ownership
│   ├── repositories/
│   ├── services/
│   ├── ingestion/
│   ├── profiling/
│   ├── semantics/
│   ├── relationships/
│   ├── capabilities/
│   ├── llm/
│   ├── models/
│   ├── simulation/
│   ├── synthetic/
│   ├── trust/
│   ├── explainability/
│   ├── jobs/
│   ├── reports/
│   └── observability/
├── data/{uploads,staging,quarantine,processed}/
├── artifacts/{models,manifests,reports,sdv}/
├── database/{migrations,sql}/
├── tests/
├── config/
├── schemas/
├── scripts/
├── docs/
└── .github/
```

Exact source-file counts are planning estimates, not a contractual architecture constraint. Prefer cohesive modules over artificially meeting a count.

## Canonical ownership rules

- SQLAlchemy ORM entities are defined exactly once under `backend/ipsp/database/models/`.
- Pydantic API request/response schemas live under `backend/ipsp/api/schemas/`; domain packages may own non-API typed contracts but may not redefine ORM entities.
- FastAPI routes live only under `backend/ipsp/api/routes/`. Authentication and other domain packages own services and policies, not duplicate routers.
- `database/migrations/` is the single repository-wide Alembic history. No package-local migration root is permitted.
