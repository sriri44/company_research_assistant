"""OpenRouter client — the only module that knows OpenRouter's chat
completions request/response shape.

One reusable client, one method (`chat_completion`) used for exactly one
call per research run — see `research_report_service.py` for why only one
AI call is made per pipeline run.
"""

from __future__ import annotations

from typing import Any

from app.clients.http_client import AsyncHttpClient, HttpClientError
from app.core.exceptions import AIProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)


class OpenRouterClient:
    def __init__(self, api_key: str, base_url: str, http_client: AsyncHttpClient) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._http = http_client

    async def chat_completion(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        json_response: bool = True,
    ) -> str:
        """Send a single chat completion request and return the raw
        assistant message content (expected to be a JSON string when
        `json_response=True`). Raises `AIProviderError` if the API key is
        missing or the request ultimately fails after retries."""
        if not self._api_key:
            raise AIProviderError("OPENROUTER_API_KEY is not configured.")

        payload: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        if json_response:
            payload["response_format"] = {"type": "json_object"}

        try:
            data = await self._http.request_json(
                "POST",
                f"{self._base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
        except HttpClientError as exc:
            logger.warning("OpenRouter request failed for model=%r: %s", model, exc)
            raise AIProviderError(f"OpenRouter request failed: {exc}") from exc

        try:
            return str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise AIProviderError("OpenRouter returned an unexpected response shape.") from exc
