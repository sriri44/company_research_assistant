"""Application entry point — FastAPI app factory.

Assembles configuration, logging, the dependency container, middleware,
exception handlers, and routers. Intentionally minimal on behavior in this
phase: the app boots, serves health checks, and exposes a versioned API
surface that returns 501 until each resource's real implementation lands
(see docs/ROADMAP.md).
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_v1_router
from app.api.v1.routes import health_routes
from app.core.config import get_settings
from app.core.container import get_container
from app.core.logging import configure_logging
from app.middleware.cors import setup_cors
from app.middleware.error_handler import register_exception_handlers
from app.middleware.error_logging import ErrorLoggingMiddleware
from app.middleware.gzip import setup_gzip
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.timing import TimingMiddleware
from app.middleware.trusted_hosts import setup_trusted_hosts
from app.utils.logger import get_logger

_DESCRIPTION = """
Backend API for the **AI Company Research Assistant**.

Given a company name or website URL, the full pipeline (in later phases)
searches the web, crawls the company's site, runs AI analysis, identifies
competitors, and surfaces **AI Growth Opportunities™** — ranked automation
ideas with estimated business impact, implementation complexity, and
priority.

This phase (backend infrastructure) ships the application skeleton:
configuration, logging, middleware, error handling, health checks, and a
versioned API surface. Resource endpoints return `501 Not Implemented`
until their service is built — see `docs/ROADMAP.md`.
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = get_logger(__name__)

    get_container()  # construct the service container once, up front

    logger.info(
        "%s v%s starting up in %r mode (debug=%s)",
        settings.app_name,
        settings.app_version,
        settings.app_env,
        settings.debug,
    )
    yield
    logger.info("%s shutting down", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=_DESCRIPTION,
        lifespan=lifespan,
    )

    # Middleware is applied outermost-first in reverse of registration
    # order: TrustedHost -> CORS -> SecurityHeaders -> GZip -> RequestId ->
    # Timing -> ErrorLogging -> routes.
    app.add_middleware(ErrorLoggingMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestIdMiddleware)
    setup_gzip(app)
    app.add_middleware(SecurityHeadersMiddleware)
    setup_cors(app, settings)
    setup_trusted_hosts(app, settings)

    register_exception_handlers(app)

    app.include_router(health_routes.router)
    app.include_router(api_v1_router)

    return app


app = create_app()
