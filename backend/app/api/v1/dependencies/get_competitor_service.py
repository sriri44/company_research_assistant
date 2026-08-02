"""FastAPI dependency provider for `CompetitorService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.competitor_service import CompetitorService


def get_competitor_service() -> CompetitorService:
    return get_container().competitor_service
