"""SearchService interface.

Responsibility: given a resolved `Company`, find candidate web results
(company site pages, news, profiles) via a search provider (Serper.dev).

Out of scope: fetching/parsing page content (that's `CrawlerService`) and
interpreting results (that's `AIService`/`CompetitorService`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.company import Company


class SearchService(ABC):
    @abstractmethod
    async def search_company(self, company: Company, limit: int = 10) -> list[str]:
        """Return candidate result URLs relevant to the given company."""
        raise NotImplementedError

    @abstractmethod
    async def search_query(self, query: str, limit: int = 10) -> list[str]:
        """Return result URLs for an arbitrary search query (e.g., used by
        `CompetitorService` to search "<company> competitors")."""
        raise NotImplementedError
