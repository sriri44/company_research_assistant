"""Unit tests for SerperClient and SerperSearchService — the HTTP layer is
mocked (AsyncHttpClient.request_json), no real network calls are made.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.clients.http_client import HttpClientError
from app.core.exceptions import SearchProviderError
from app.models.company import Company
from app.search.serper_client import SerperClient
from app.services.implementations.serper_search_service import SerperSearchService


def _fake_http_client(payload: dict) -> AsyncMock:
    http_client = AsyncMock()
    http_client.request_json = AsyncMock(return_value=payload)
    return http_client


@pytest.mark.asyncio
async def test_serper_client_parses_organic_results_and_knowledge_graph() -> None:
    http_client = _fake_http_client(
        {
            "organic": [
                {
                    "title": "Stripe",
                    "link": "https://stripe.com",
                    "snippet": "Payments infrastructure.",
                },
                {"title": "No link here"},  # missing "link" — should be skipped
            ],
            "knowledgeGraph": {
                "title": "Stripe",
                "website": "https://stripe.com",
                "type": "Company",
                "description": "Online payment processing.",
            },
        }
    )
    client = SerperClient("test-key", "https://google.serper.dev", http_client)

    result = await client.search("stripe")

    assert len(result.organic) == 1
    assert result.organic[0].link == "https://stripe.com"
    assert result.knowledge_graph is not None
    assert result.knowledge_graph.website == "https://stripe.com"


@pytest.mark.asyncio
async def test_serper_client_raises_search_provider_error_without_api_key() -> None:
    client = SerperClient("", "https://google.serper.dev", AsyncMock())

    with pytest.raises(SearchProviderError):
        await client.search("stripe")


@pytest.mark.asyncio
async def test_serper_client_wraps_http_failures_as_search_provider_error() -> None:
    http_client = AsyncMock()
    http_client.request_json = AsyncMock(side_effect=HttpClientError("boom"))
    client = SerperClient("test-key", "https://google.serper.dev", http_client)

    with pytest.raises(SearchProviderError):
        await client.search("stripe")


@pytest.mark.asyncio
async def test_search_service_search_company_excludes_own_domain() -> None:
    http_client = _fake_http_client(
        {
            "organic": [
                {"title": "Self", "link": "https://stripe.com/about"},
                {"title": "Competitor", "link": "https://adyen.com"},
            ]
        }
    )
    client = SerperClient("test-key", "https://google.serper.dev", http_client)
    service = SerperSearchService(client)
    company = Company(id="1", name="Stripe", domain="stripe.com")

    links = await service.search_company(company, limit=10)

    assert links == ["https://adyen.com"]


@pytest.mark.asyncio
async def test_search_service_search_query_returns_all_links() -> None:
    http_client = _fake_http_client({"organic": [{"title": "A", "link": "https://a.com"}]})
    client = SerperClient("test-key", "https://google.serper.dev", http_client)
    service = SerperSearchService(client)

    links = await service.search_query("some query", limit=10)

    assert links == ["https://a.com"]
