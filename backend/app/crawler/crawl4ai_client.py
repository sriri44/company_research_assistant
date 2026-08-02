"""Crawl4AI client — the only module that imports `crawl4ai` directly.

Wraps a single shared `AsyncWebCrawler` browser session (reused across
every page fetched for one research run, per the "no duplicate crawling /
reuse HTTP client" performance requirement) and normalizes results into
`CrawledPage` + the raw internal links found on that page, translating any
failure into `CrawlerError` so callers never see a raw crawl4ai exception.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

from app.core.exceptions import CrawlerError
from app.crawler.types import CrawledPage
from app.utils.logger import get_logger

logger = get_logger(__name__)

_EXCLUDED_TAGS = ["nav", "footer", "script", "style", "form", "iframe", "noscript"]


@dataclass(frozen=True)
class Crawl4AIPageResult:
    page: CrawledPage
    internal_link_hrefs: list[str] = field(default_factory=list)


class Crawl4AIClient:
    """Async-context-managed wrapper: `async with Crawl4AIClient(...) as client:`
    then `await client.fetch(url)` for each page in the crawl."""

    def __init__(self, *, user_agent: str, page_timeout_seconds: int = 30) -> None:
        self._browser_config = BrowserConfig(user_agent=user_agent, headless=True, verbose=False)
        self._run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            word_count_threshold=20,
            excluded_tags=_EXCLUDED_TAGS,
            exclude_external_links=True,
            remove_overlay_elements=True,
            page_timeout=page_timeout_seconds * 1000,
            verbose=False,
        )
        self._crawler: AsyncWebCrawler | None = None

    async def __aenter__(self) -> Crawl4AIClient:
        crawler = AsyncWebCrawler(config=self._browser_config)
        try:
            await crawler.start()
        except Exception as exc:
            # Most commonly: the Playwright browser binary isn't installed
            # (needs `playwright install chromium` in addition to `pip
            # install`, which is easy to miss in a deploy's build step).
            # Not a CrawlerError-subclass upstream, so it must be caught
            # and translated here — otherwise it's an unhandled exception
            # that skips the rest of the pipeline's graceful degradation.
            logger.warning("Failed to start crawler browser session: %s", exc.__class__.__name__)
            raise CrawlerError("Failed to start the crawler browser session.") from exc
        self._crawler = crawler
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        if self._crawler is not None:
            await self._crawler.close()
            self._crawler = None

    async def fetch(self, url: str) -> Crawl4AIPageResult:
        """Fetch one URL, returning its cleaned content and the internal
        links discovered on it in a single request."""
        if self._crawler is None:
            raise CrawlerError("Crawl4AIClient used outside of its async context manager.")

        try:
            result = await self._crawler.arun(url=url, config=self._run_config)
        except Exception as exc:  # crawl4ai raises assorted exception types internally
            logger.warning("Crawl raised an exception for %s: %s", url, exc.__class__.__name__)
            raise CrawlerError(f"Failed to crawl {url}") from exc

        if not result.success:
            raise CrawlerError(f"Failed to crawl {url}: {result.error_message or 'unknown error'}")

        title = result.metadata.get("title") if result.metadata else None
        page = CrawledPage(url=url, title=title, text_content=str(result.markdown or ""))

        internal_links = (result.links or {}).get("internal", [])
        hrefs = [str(link["href"]) for link in internal_links if link.get("href")]

        return Crawl4AIPageResult(page=page, internal_link_hrefs=hrefs)
