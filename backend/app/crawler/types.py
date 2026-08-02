"""Crawler-local data shapes.

`CrawledPage` is intentionally kept out of `app.models` because it is a
crawler implementation detail (raw normalized page content), not a core
business domain concept. Services consume it only through
`CrawlerService`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CrawledPage:
    url: str
    title: str | None
    text_content: str
    html_content: str | None = None
