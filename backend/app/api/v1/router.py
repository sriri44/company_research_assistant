"""API v1 router aggregator.

Collects every versioned resource router under a single `/api/v1` prefix.
The unversioned root health probes (`health_routes.router`) are mounted
directly on the app in `app.main`, not here — see that module's docstring
for why.
"""

from fastapi import APIRouter

from app.api.v1.routes import (
    company_routes,
    opportunity_routes,
    report_routes,
    research_routes,
    system_routes,
)

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(company_routes.router)
api_v1_router.include_router(research_routes.router)
api_v1_router.include_router(report_routes.router)
api_v1_router.include_router(opportunity_routes.router)
api_v1_router.include_router(system_routes.router)
