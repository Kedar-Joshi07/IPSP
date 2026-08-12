"""Single canonical router registration point."""

from fastapi import APIRouter

from ipsp.api.routes import auth_router, health_router, root_router


def build_router() -> APIRouter:
    """Build a fresh router for an application instance."""
    router = APIRouter()
    router.include_router(health_router)
    router.include_router(root_router, prefix="/api/v1", tags=["system"])
    router.include_router(auth_router, prefix="/api/v1")
    return router
