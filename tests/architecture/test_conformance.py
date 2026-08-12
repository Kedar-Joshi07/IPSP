"""Foundation architecture and contamination guardrails."""

import re
from pathlib import Path

from ipsp.database.models import Base

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND = PROJECT_ROOT / "backend" / "ipsp"
FRONTEND = PROJECT_ROOT / "frontend"
MIGRATIONS = PROJECT_ROOT / "database" / "migrations"


def _read_production_source() -> str:
    paths = list(BACKEND.rglob("*.py"))
    paths.extend(
        path for path in FRONTEND.rglob("*") if path.suffix.lower() in {".html", ".css", ".js"}
    )
    paths.extend(MIGRATIONS.rglob("*.py"))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_production_source_has_no_prohibited_architecture_patterns() -> None:
    source = _read_production_source()
    lowered = source.lower()

    for prohibited in (
        "streamlit",
        "session.query(",
        "asyncsession",
        "create_async_engine",
        "aiosqlite",
        "metadata.create_all",
        ".create_all(",
        "python-jose",
        "jsonwebtoken",
        "import jwt",
        "import redis",
        "from redis",
        "import celery",
        "from celery",
        "bcrypt",
        "passlib",
        "pyjwt",
        "user_preferences",
    ):
        assert prohibited not in lowered
    for network_import in (
        "import requests",
        "import httpx",
        "from httpx",
        "import aiohttp",
        "urllib.request",
    ):
        assert network_import not in lowered


def test_phase1f_has_one_declarative_base_and_exact_security_table_allowlist() -> None:
    source = _read_production_source()
    model_declaration_files = [
        path
        for path in BACKEND.rglob("*.py")
        if "__tablename__" in path.read_text(encoding="utf-8")
    ]

    assert re.findall(r"class\s+\w+\(DeclarativeBase\)", source) == ["class Base(DeclarativeBase)"]
    assert model_declaration_files == [BACKEND / "database" / "models" / "security.py"]
    assert set(Base.metadata.tables) == {
        "permissions",
        "role_permissions",
        "roles",
        "user_sessions",
        "users",
    }


def test_phase1f_rbac_ownership_is_canonical() -> None:
    rbac_service_files = [
        path
        for path in BACKEND.rglob("*.py")
        if "class RBACService" in path.read_text(encoding="utf-8")
    ]
    permission_repository_files = [
        path
        for path in BACKEND.rglob("*.py")
        if "class PermissionRepository" in path.read_text(encoding="utf-8")
    ]
    permission_dependency_files = [
        path
        for path in BACKEND.rglob("*.py")
        if "def require_permission(" in path.read_text(encoding="utf-8")
    ]

    assert rbac_service_files == [BACKEND / "auth" / "rbac.py"]
    assert permission_repository_files == [BACKEND / "repositories" / "rbac.py"]
    assert permission_dependency_files == [BACKEND / "api" / "dependencies" / "rbac.py"]

    route_source = "\n".join(
        path.read_text(encoding="utf-8") for path in (BACKEND / "api" / "routes").rglob("*.py")
    )
    dependency_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (BACKEND / "api" / "dependencies").rglob("*.py")
    )
    for database_pattern in (
        "sqlalchemy",
        "select(",
        "session.execute(",
        "session.scalars(",
        "session.query(",
    ):
        assert database_pattern not in (route_source + dependency_source).lower()


def test_phase1f_has_no_runtime_role_name_authorization_or_session_snapshot() -> None:
    rbac_source = (BACKEND / "auth" / "rbac.py").read_text(encoding="utf-8")
    session_columns = set(Base.metadata.tables["user_sessions"].columns.keys())

    assert "role.name" not in rbac_source
    assert '== "Admin"' not in rbac_source
    assert "BaseRepository" not in _read_production_source()
    assert {
        "permissions",
        "permission_codes",
        "permission_snapshot",
        "role_name",
        "is_admin",
    }.isdisjoint(session_columns)


def test_phase1d_security_schema_has_no_authorization_bypass_columns() -> None:
    prohibited_columns = {
        "is_admin",
        "is_superuser",
        "admin_flag",
        "superuser",
        "permission_level",
        "access_level",
    }

    for table in Base.metadata.tables.values():
        assert prohibited_columns.isdisjoint(table.columns.keys())


def test_generic_core_has_no_benchmark_specific_output_terms() -> None:
    lowered = _read_production_source().lower()

    for term in ("campaignsim", "campaign", "funnel_stage", "roas", "cpa", "faiss", "xgboost"):
        assert term not in lowered


def test_frontend_has_no_runtime_cdn_reference() -> None:
    frontend_source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix.lower() in {".html", ".css", ".js"}
    ).lower()

    for term in ("cdnjs", "unpkg.com", "jsdelivr.net"):
        assert term not in frontend_source
    for framework in ("react", "vue", "angular"):
        assert framework not in frontend_source


def test_there_is_exactly_one_alembic_history_root() -> None:
    def is_repository_source(path: Path) -> bool:
        return not any(part == ".git" or part.startswith(".venv") for part in path.parts)

    migration_environments = [
        path for path in PROJECT_ROOT.rglob("env.py") if is_repository_source(path)
    ]
    alembic_configs = [
        path for path in PROJECT_ROOT.rglob("alembic.ini") if is_repository_source(path)
    ]
    script_templates = [
        path for path in PROJECT_ROOT.rglob("script.py.mako") if is_repository_source(path)
    ]

    assert migration_environments == [PROJECT_ROOT / "database" / "migrations" / "env.py"]
    assert alembic_configs == [PROJECT_ROOT / "alembic.ini"]
    assert script_templates == [PROJECT_ROOT / "database" / "migrations" / "script.py.mako"]
