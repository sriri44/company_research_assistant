"""System-facing schemas: health/readiness status and app version info.

Backs the root-level health endpoints (`app.api.v1.routes.health_routes`)
and, later, `/api/v1/system`. Neither of these schemas is ever built from
data that required calling an external service.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    timestamp: str


class VersionResponse(BaseModel):
    app_name: str
    app_version: str
    app_env: str
