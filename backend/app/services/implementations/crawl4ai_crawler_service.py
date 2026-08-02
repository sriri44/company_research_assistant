"""Crawl4AI-backed CrawlerService implementation.

`crawl_many` treats the given URLs as seed pages for one company's site:
it fetches them (bounded concurrency, one shared browser session), then —
if the seeds didn't yield `max_pages` worth of content — expands into
allow-listed internal links discovered on those seed pages until the page
cap is reached. Never crawls more than `max_pages` pages and never
fetches the same URL twice within one call (both via `path_discovery`'s
dedup and the shared `already_seen` set below).
"""

from __future__ import annotations

import asyncio

from app.core.exceptions import CrawlerError
from app.crawler.crawl4ai_client import Crawl4AIClient, Crawl4AIPageResult
from app.crawler.strategies.path_discovery import filter_internal_links
from app.crawler.types import CrawledPage
from app.services.interfaces.crawler_service import CrawlerService
from app.utils.logger import get_logger

logger = get_logger(__name__)

_CONCURRENCY = 3


class Crawl4AICrawlerService(CrawlerService):
    def __init__(self, *, user_agent: str, max_pages: int, page_timeout_seconds: int) -> None:
        self._user_agent = user_agent
        self._max_pages = max_pages
        self._page_timeout_seconds = page_timeout_seconds

    async def crawl(self, url: str) -> CrawledPage:
        async with Crawl4AIClient(
            user_agent=self._user_agent, page_timeout_seconds=self._page_timeout_seconds
        ) as client:
            result = await client.fetch(url)
            return result.page

    async def crawl_many(self, urls: list[str]) -> list[CrawledPage]:
        if not urls:
            return []

        seen: set[str] = set(urls)
        pages: list[CrawledPage] = []
        discovered_links: list[str] = []

        async with Crawl4AIClient(
            user_agent=self._user_agent, page_timeout_seconds=self._page_timeout_seconds
        ) as client:
            seed_results = await self._fetch_many(client, urls[: self._max_pages])
            for seed_url, result in seed_results:
                if result is None:
                    continue
                pages.append(result.page)
                discovered_links.extend(
                    filter_internal_links(seed_url, result.internal_link_hrefs, already_seen=seen)
                )

            remaining_budget = self._max_pages - len(pages)
            if remaining_budget > 0 and discovered_links:
                extra_results = await self._fetch_many(client, discovered_links[:remaining_budget])
                pages.extend(result.page for _url, result in extra_results if result is not None)

        logger.info("Crawled %d page(s) from %d seed URL(s)", len(pages), len(urls))
        return pages[: self._max_pages]

    async def _fetch_many(
        self, client: Crawl4AIClient, urls: list[str]
    ) -> list[tuple[str, Crawl4AIPageResult | None]]:
        semaphore = asyncio.Semaphore(_CONCURRENCY)

        async def fetch_one(url: str) -> tuple[str, Crawl4AIPageResult | None]:
            async with semaphore:
                try:
                    return url, await client.fetch(url)
                except CrawlerError as exc:
                    logger.warning("Skipping page (crawl failed): %s", exc)
                    return url, None

        return await asyncio.gather(*(fetch_one(url) for url in urls))
