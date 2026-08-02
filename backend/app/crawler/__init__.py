"""Crawler boundary.

`crawl4ai_client.py` is the only module that imports `crawl4ai` directly.
`CrawlerService` (see `app.services.interfaces.crawler_service`, backed by
`app.services.implementations.crawl4ai_crawler_service`) is the public
contract other layers depend on; `strategies/` decides which pages are
worth crawling.
"""
