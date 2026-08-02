"""FastAPI dependency provider for `CrawlerService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.crawler_service import CrawlerService


def get_crawler_service() -> CrawlerService:
    return get_container().crawler_service
