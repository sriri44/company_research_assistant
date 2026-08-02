"""FastAPI dependency provider for `OpportunityService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.opportunity_service import OpportunityService


def get_opportunity_service() -> OpportunityService:
    return get_container().opportunity_service
