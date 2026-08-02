"""CrawlerService interface.

Responsibility: given one or more URLs, fetch and normalize page content
(via Crawl4AI). Purely mechanical content extraction — no interpretation.

Out of scope: deciding *which* URLs to crawl (that's `SearchService`'s
output feeding in) and interpreting the extracted content (that's
`AIService`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.crawler.types import CrawledPage


class CrawlerService(ABC):
    @abstractmethod
    async def crawl(self, url: str) -> CrawledPage:
        """Fetch and normalize a single page."""
        raise NotImplementedError

    @abstractmethod
    async def crawl_many(self, urls: list[str]) -> list[CrawledPage]:
        """Fetch and normalize multiple pages, tolerating individual
        failures without aborting the whole batch."""
        raise NotImplementedError
