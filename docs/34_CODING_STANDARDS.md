# Coding Standards

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
