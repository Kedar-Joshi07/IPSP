"""FastAPI application factory for the IPSP foundation."""

from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from ipsp.api.router import build_router
from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Settings
from ipsp.errors.handlers import register_exception_handlers
from ipsp.jobs.contracts import JobHandler
from ipsp.jobs.enums import JobType
from ipsp.observability.context import RequestContextMiddleware
from ipsp.observability.logging import configure_logging


def create_app(
    settings: Settings | None = None,
    *,
    job_handlers: Mapping[JobType, JobHandler] | None = None,
) -> FastAPI:
    """Construct an isolated application instance with foundation services only."""
    app_settings = settings or Settings()
    foundation_services = build_foundation_services(app_settings, job_handlers=job_handlers)
    configure_logging(app_settings.log_level, app_settings.log_dir)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        readiness = await run_in_threadpool(foundation_services.readiness_service.check)
        if readiness.ready:
            await run_in_threadpool(foundation_services.job_backend.start)
        try:
            yield
        finally:
            foundation_services.job_backend.shutdown()

    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        debug=app_settings.debug,
        lifespan=lifespan,
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
