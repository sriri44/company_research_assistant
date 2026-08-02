"""Unit tests for OpenRouterClient — the HTTP layer is mocked
(AsyncHttpClient.request_json), no real network calls are made.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.ai.openrouter_client import OpenRouterClient
from app.clients.http_client import HttpClientError
from app.core.exceptions import AIProviderError


@pytest.mark.asyncio
async def test_chat_completion_returns_message_content() -> None:
    http_client = AsyncMock()
    http_client.request_json = AsyncMock(
        return_value={"choices": [{"message": {"content": '{"ok": true}'}}]}
    )
    client = OpenRouterClient("test-key", "https://openrouter.ai/api/v1", http_client)

    content = await client.chat_completion(
        model="openai/gpt-4o-mini", system_prompt="system", user_prompt="user"
    )

    assert content == '{"ok": true}'


@pytest.mark.asyncio
async def test_chat_completion_raises_without_api_key() -> None:
    client = OpenRouterClient("", "https://openrouter.ai/api/v1", AsyncMock())

    with pytest.raises(AIProviderError):
        await client.chat_completion(model="m", system_prompt="s", user_prompt="u")


@pytest.mark.asyncio
async def test_chat_completion_wraps_http_failures() -> None:
    http_client = AsyncMock()
    http_client.request_json = AsyncMock(side_effect=HttpClientError("timeout"))
    client = OpenRouterClient("test-key", "https://openrouter.ai/api/v1", http_client)

    with pytest.raises(AIProviderError):
        await client.chat_completion(model="m", system_prompt="s", user_prompt="u")


@pytest.mark.asyncio
async def test_chat_completion_raises_on_unexpected_response_shape() -> None:
    http_client = AsyncMock()
    http_client.request_json = AsyncMock(return_value={"unexpected": "shape"})
    client = OpenRouterClient("test-key", "https://openrouter.ai/api/v1", http_client)

    with pytest.raises(AIProviderError):
        await client.chat_completion(model="m", system_prompt="s", user_prompt="u")
