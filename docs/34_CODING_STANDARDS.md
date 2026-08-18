# Coding Standards

Apply these standards within the authority boundaries of the
[F-002 Architecture Freeze](44_F002_ARCHITECTURE_FREEZE.md) and the accepted workstream contract.

## Python
- Type hints required on public interfaces.
- Pydantic for API/structured provider contracts.
- Services/repositories/engines have single coherent responsibilities.
- Avoid oversized god classes and circular imports.
- Docstrings for public classes/functions where behavior is not obvious.
- Use explicit enums/value objects for statuses, roles, capability types, error codes.
- Configuration from typed settings, not scattered environment lookups.

## SQL/database
- Migrations only; repositories mediate data access.
- Transactions around state transitions.
- Foreign keys and uniqueness constraints where semantically valid.
- Define each SQLAlchemy ORM entity once under `backend/ipsp/database/models/`; keep Pydantic API schemas separate.
- Use synchronous SQLAlchemy 2.x `select()`/`Session.execute()`/`Session.scalars()` for the SQLite control plane. Do not use `Session.query()` or wrap blocking Session work in `async def`.
- Maintain one Alembic history under `database/migrations/`.

## API
- FastAPI route modules live under `backend/ipsp/api/routes/` and remain thin.
- Domain packages provide services and policies and do not define duplicate routers.
- Versioned contracts keep Dataset Semantic Manifest, Domain Experience, Metric/Formula,
  CrossDomainSemanticGraph, capability, engine/license, ScenarioIntentManifest,
  CompositeSimulationGraph, Trust, Evidence Profile, learning, and outcome authorities distinct.
- Safe limitation/refusal responses are first-class API behavior; providers may not silently alter
  intent, basis, evidence class, formula, semantic relation, or license decision.

## Providers and computation

- Application services depend on typed IPSP interfaces; vendor libraries remain adapters.
- Resolve semantic/data capability before engine family and provider eligibility.
- Formula execution uses a constrained typed representation, never arbitrary Python/SQL/LLM code.
- Synthetic, simulation, assumption, external, benchmark, and LLM values retain provenance and do
  not enter observed data or empirical training sets through convenience paths.
- Reproduce uses exact immutable versions and evidence snapshots; re-run with current eligible
  versions is a distinct operation.

## JavaScript
- ES modules.
- Central API client/state/theme/auth utilities.
- Avoid inline business logic in HTML.
- Dynamic rendering must be driven by API contracts.

## CSS
- Shared tokens and component classes.
- No page-specific color systems that break the application identity.
- Dark/light theme via variables.

## Comments
Explain why/constraint/business meaning, not line-by-line obvious syntax.
