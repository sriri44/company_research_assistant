"""Placeholder CrawlerService.

Satisfies the `CrawlerService` interface so the DI graph and API layer are
wireable before a real Crawl4AI-backed implementation exists. See
docs/ROADMAP.md Phase 2.
"""

from __future__ import annotations

from app.crawler.types import CrawledPage
from app.services.interfaces.crawler_service import CrawlerService


class PlaceholderCrawlerService(CrawlerService):
    async def crawl(self, url: str) -> CrawledPage:
        raise NotImplementedError(
            "CrawlerService.crawl is not implemented yet — see docs/ROADMAP.md"
        )

    async def crawl_many(self, urls: list[str]) -> list[CrawledPage]:
        raise NotImplementedError(
            "CrawlerService.crawl_many is not implemented yet — see docs/ROADMAP.md"
        )
