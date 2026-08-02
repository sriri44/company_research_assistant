"""Serper.dev client.

Thin wrapper around Serper's `/search` endpoint — the only place in the
codebase that knows Serper's request/response shape. Consumed by
`app.services.implementations.serper_search_service` (the `SearchService`
implementation) and by `DefaultCompanyService` for name -> website
resolution grounding.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.clients.http_client import AsyncHttpClient, HttpClientError
from app.core.exceptions import SearchProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class SerperOrganicResult:
    title: str
    link: str
    snippet: str | None = None


@dataclass(frozen=True)
class SerperKnowledgeGraph:
    title: str | None = None
    website: str | None = None
    entity_type: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class SerperSearchResult:
    organic: list[SerperOrganicResult] = field(default_factory=list)
    knowledge_graph: SerperKnowledgeGraph | None = None


class SerperClient:
    """Wraps Serper.dev's `/search` endpoint (Google search results)."""

    def __init__(self, api_key: str, base_url: str, http_client: AsyncHttpClient) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._http = http_client

    async def search(self, query: str, num: int = 10) -> SerperSearchResult:
        """Run a search via Serper, returning organic results plus the
        knowledge graph if Serper found one. Raises `SearchProviderError`
        if the API key is missing or the request ultimately fails after
        retries — never raises a raw httpx/HttpClientError."""
        if not self._api_key:
            raise SearchProviderError("SERPER_API_KEY is not configured.")

        try:
            payload = await self._http.request_json(
                "POST",
                f"{self._base_url}/search",
                headers={"X-API-KEY": self._api_key, "Content-Type": "application/json"},
                json={"q": query, "num": num},
            )
        except HttpClientError as exc:
            logger.warning("Serper search failed for query=%r: %s", query, exc)
            raise SearchProviderError(f"Serper search failed: {exc}") from exc

        return _parse_search_response(payload)


def _parse_search_response(payload: dict[str, Any]) -> SerperSearchResult:
    organic = [
        SerperOrganicResult(
            title=item.get("title", ""),
            link=item["link"],
            snippet=item.get("snippet"),
        )
        for item in payload.get("organic", [])
        if item.get("link")
    ]

    kg_payload = payload.get("knowledgeGraph")
    knowledge_graph = (
        SerperKnowledgeGraph(
            title=kg_payload.get("title"),
            website=kg_payload.get("website"),
            entity_type=kg_payload.get("type"),
            description=kg_payload.get("description"),
        )
        if kg_payload
        else None
    )

    return SerperSearchResult(organic=organic, knowledge_graph=knowledge_graph)
