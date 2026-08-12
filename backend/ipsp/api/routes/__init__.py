"""Thin FastAPI route modules."""

from ipsp.api.routes.auth import router as auth_router
from ipsp.api.routes.health import router as health_router
from ipsp.api.routes.jobs import router as jobs_router
from ipsp.api.routes.root import router as root_router

__all__ = ["auth_router", "health_router", "jobs_router", "root_router"]
