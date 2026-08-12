"""Thin FastAPI route modules."""

from ipsp.api.routes.admin_system import router as admin_system_router
from ipsp.api.routes.auth import router as auth_router
from ipsp.api.routes.health import router as health_router
from ipsp.api.routes.jobs import router as jobs_router
from ipsp.api.routes.root import router as root_router

__all__ = ["admin_system_router", "auth_router", "health_router", "jobs_router", "root_router"]
