"""FastAPI dependency provider for `SearchService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.search_service import SearchService


def get_search_service() -> SearchService:
    return get_container().search_service
