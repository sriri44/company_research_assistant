"""Serper-backed SearchService implementation.

`search_query` is a generic passthrough (used by `DefaultCompanyService`
for name -> website resolution). `search_company` runs a
competitor-oriented query by default — its main real use in this phase is
grounding competitor discovery in actual search results rather than
letting the AI invent competitors from nothing.
"""

from __future__ import annotations

from app.models.company import Company
from app.search.serper_client import SerperClient
from app.services.interfaces.search_service import SearchService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SerperSearchService(SearchService):
    def __init__(self, serper_client: SerperClient) -> None:
        self._client = serper_client

    async def search_company(self, company: Company, limit: int = 10) -> list[str]:
        result = await self._client.search(f"{company.name} competitors alternatives", num=limit)
        return [
            link for link in (item.link for item in result.organic) if company.domain not in link
        ][:limit]

    async def search_query(self, query: str, limit: int = 10) -> list[str]:
        result = await self._client.search(query, num=limit)
        return [item.link for item in result.organic][:limit]
