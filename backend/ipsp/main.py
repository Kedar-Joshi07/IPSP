"""FastAPI application factory for the IPSP foundation."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ipsp.api.router import build_router
from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Settings
from ipsp.errors.handlers import register_exception_handlers
from ipsp.observability.context import RequestContextMiddleware
from ipsp.observability.logging import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    """Construct an isolated application instance with foundation services only."""
    app_settings = settings or Settings()
    foundation_services = build_foundation_services(app_settings)
    configure_logging(app_settings.log_level)

    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        debug=app_settings.debug,
    )
    app.state.settings = app_settings
    app.state.foundation_services = foundation_services
    register_exception_handlers(app)
    app.add_middleware(RequestContextMiddleware)
    app.include_router(build_router())

    if app_settings.frontend_dir.is_dir():
        app.mount(
            "/",
            StaticFiles(directory=app_settings.frontend_dir, html=True),
            name="frontend",
        )

    return app
