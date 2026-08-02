"""Unit tests for OpenRouterAIService — the OpenRouterClient is mocked, no
real network calls are made. Uses the real `research_analysis` prompt
template so these tests also catch template/placeholder regressions.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel

from app.core.exceptions import AIProviderError
from app.services.implementations.openrouter_ai_service import OpenRouterAIService

_VALID_ANALYSIS_JSON = json.dumps(
    {
        "company_name": "Acme Corp",
        "website": "acme.com",
        "phone": None,
        "address": None,
        "summary": "A widget company.",
        "industry": "Manufacturing",
        "products": ["Widgets"],
        "services": [],
        "pain_points": ["Manual order processing"],
        "competitors": [
            {
                "name": "Widgets Inc",
                "website": "widgetsinc.com",
                "reason": "Direct competitor",
                "market_position": "Leader",
            }
        ],
        "growth_opportunities": [
            {
                "title": "Automate order intake",
                "description": "Use AI to parse incoming orders.",
                "business_impact": "high",
                "implementation_complexity": "medium",
                "priority_score": 88,
                "estimated_roi": "20% faster processing",
            }
        ],
        "sources": ["https://acme.com"],
        "confidence": 0.8,
    }
)


class _SampleResponseModel(BaseModel):
    company_name: str
    confidence: float


def _make_service(chat_response: str) -> tuple[OpenRouterAIService, AsyncMock]:
    client = AsyncMock()
    client.chat_completion = AsyncMock(return_value=chat_response)
    service = OpenRouterAIService(client, default_model="default/model")
    return service, client


@pytest.mark.asyncio
async def test_generate_renders_prompt_and_uses_default_model() -> None:
    service, client = _make_service("plain text response")

    result = await service.generate(
        "research_analysis",
        {
            "company_name": "Acme Corp",
            "website": "acme.com",
            "context": "Acme makes widgets.",
            "competitor_hints": "- https://widgetsinc.com",
        },
    )

    assert result == "plain text response"
    call_kwargs = client.chat_completion.call_args.kwargs
    assert call_kwargs["model"] == "default/model"
    assert "Acme Corp" in call_kwargs["user_prompt"]
    assert "Acme makes widgets." in call_kwargs["user_prompt"]
    assert "{{" not in call_kwargs["user_prompt"]  # every placeholder was substituted


@pytest.mark.asyncio
async def test_generate_uses_model_from_context_when_provided() -> None:
    service, client = _make_service("plain text response")

    await service.generate(
        "research_analysis",
        {
            "company_name": "Acme",
            "website": "acme.com",
            "context": "x",
            "competitor_hints": "x",
            "model": "openai/gpt-4o",
        },
    )

    assert client.chat_completion.call_args.kwargs["model"] == "openai/gpt-4o"


@pytest.mark.asyncio
async def test_generate_structured_parses_valid_json() -> None:
    service, _ = _make_service(json.dumps({"company_name": "Acme", "confidence": 0.9}))

    result = await service.generate_structured(
        "research_analysis",
        {"company_name": "Acme", "website": "acme.com", "context": "x", "competitor_hints": "x"},
        _SampleResponseModel,
    )

    assert result.company_name == "Acme"
    assert result.confidence == 0.9


@pytest.mark.asyncio
async def test_generate_structured_strips_markdown_fences() -> None:
    fenced = f"```json\n{json.dumps({'company_name': 'Acme', 'confidence': 0.5})}\n```"
    service, _ = _make_service(fenced)

    result = await service.generate_structured(
        "research_analysis",
        {"company_name": "Acme", "website": "acme.com", "context": "x", "competitor_hints": "x"},
        _SampleResponseModel,
    )

    assert result.company_name == "Acme"


@pytest.mark.asyncio
async def test_generate_structured_raises_on_invalid_json() -> None:
    service, _ = _make_service("this is not json at all")

    with pytest.raises(AIProviderError):
        await service.generate_structured(
            "research_analysis",
            {
                "company_name": "Acme",
                "website": "acme.com",
                "context": "x",
                "competitor_hints": "x",
            },
            _SampleResponseModel,
        )


@pytest.mark.asyncio
async def test_generate_structured_full_research_schema() -> None:
    from app.ai.schemas import ResearchAnalysisResult

    service, _ = _make_service(_VALID_ANALYSIS_JSON)

    result = await service.generate_structured(
        "research_analysis",
        {
            "company_name": "Acme Corp",
            "website": "acme.com",
            "context": "x",
            "competitor_hints": "x",
        },
        ResearchAnalysisResult,
    )

    assert result.company_name == "Acme Corp"
    assert len(result.competitors) == 1
    assert len(result.growth_opportunities) == 1
    assert result.confidence == 0.8
