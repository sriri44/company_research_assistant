"""Root-level health/liveness/version endpoints.

Mounted directly on the app (no `/api/v1` prefix) since infrastructure
health checks (Render, load balancers, uptime monitors) expect stable,
unversioned paths. None of these call an external service or a
placeholder service implementation — they only report on the app process
itself, so they stay meaningful even before Phase 2+ services exist.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.v1.dependencies.get_current_settings import get_current_settings
from app.core.config import Settings
from app.schemas.common import SuccessResponse
from app.schemas.system_schema import HealthResponse, VersionResponse
from app.utils.response_helper import build_success_response
from app.utils.time_utils import utcnow

router = APIRouter(tags=["system"])


@router.get("/", response_model=SuccessResponse[VersionResponse])
async def root(
    settings: Settings = Depends(get_current_settings),
) -> SuccessResponse[VersionResponse]:
    """Basic app identity — a friendly landing response, not a health check."""
    return build_success_response(
        VersionResponse(
            app_name=settings.app_name,
            app_version=settings.app_version,
            app_env=settings.app_env,
        )
    )


@router.get("/health", response_model=SuccessResponse[HealthResponse])
async def health() -> SuccessResponse[HealthResponse]:
    """Liveness probe: is the process up and able to handle a request."""
    return build_success_response(HealthResponse(status="ok", timestamp=utcnow().isoformat()))


@router.get("/ready", response_model=SuccessResponse[HealthResponse])
async def ready() -> SuccessResponse[HealthResponse]:
    """Readiness probe: is the process ready to accept traffic. Still makes
    no external calls in this phase — evolves once real dependencies
    (DB, upstream APIs) need checking."""
    return build_success_response(HealthResponse(status="ok", timestamp=utcnow().isoformat()))


@router.get("/version", response_model=SuccessResponse[VersionResponse])
async def version(
    settings: Settings = Depends(get_current_settings),
) -> SuccessResponse[VersionResponse]:
    """Reports the running app's name/version/environment."""
    return build_success_response(
        VersionResponse(
            app_name=settings.app_name,
            app_version=settings.app_version,
            app_env=settings.app_env,
        )
    )
