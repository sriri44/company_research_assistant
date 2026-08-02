"""Placeholder SearchService.

Satisfies the `SearchService` interface so the DI graph and API layer are
wireable before a real Serper.dev-backed implementation exists. See
docs/ROADMAP.md Phase 2.
"""

from __future__ import annotations

from app.models.company import Company
from app.services.interfaces.search_service import SearchService


class PlaceholderSearchService(SearchService):
    async def search_company(self, company: Company, limit: int = 10) -> list[str]:
        raise NotImplementedError(
            "SearchService.search_company is not implemented yet — see docs/ROADMAP.md"
        )

    async def search_query(self, query: str, limit: int = 10) -> list[str]:
        raise NotImplementedError(
            "SearchService.search_query is not implemented yet — see docs/ROADMAP.md"
        )
