"""Shared async HTTP client: retry with backoff + consistent timeout and
error handling.

Every outbound integration (`SerperClient`, `OpenRouterClient`) goes
through one `AsyncHttpClient` instance instead of constructing its own
`httpx.AsyncClient`, so connection pooling is reused and retry/timeout
behavior is defined exactly once. Never logs headers or request bodies —
API keys must never reach the logs.
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from app.utils.logger import get_logger

logger = get_logger(__name__)


class HttpClientError(Exception):
    """Raised when an HTTP request ultimately fails after retries, or
    fails immediately on a non-retryable (4xx) response."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class AsyncHttpClient:
    """Thin, reusable wrapper around `httpx.AsyncClient`. Retries on
    timeouts, connection errors, and 5xx responses with exponential
    backoff; 4xx responses fail fast since retrying an invalid request
    never helps."""

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
        backoff_seconds: float = 0.75,
    ) -> None:
        self._client = httpx.AsyncClient(timeout=timeout)
        self._max_retries = max_retries
        self._backoff_seconds = backoff_seconds

    async def request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a request and return the parsed JSON body. Raises
        `HttpClientError` if every attempt fails."""
        last_error: Exception | None = None
        attempts_made = 0

        for attempt in range(1, self._max_retries + 1):
            attempts_made = attempt
            try:
                response = await self._client.request(
                    method, url, headers=headers, json=json, params=params
                )
                if response.status_code >= 500:
                    raise HttpClientError(
                        f"Upstream error {response.status_code}",
                        status_code=response.status_code,
                    )
                if response.status_code >= 400:
                    raise HttpClientError(
                        f"Request rejected with status {response.status_code}",
                        status_code=response.status_code,
                    )
                body: dict[str, Any] = response.json()
                return body
            except (httpx.TimeoutException, httpx.TransportError, HttpClientError) as exc:
                last_error = exc
                non_retryable = isinstance(exc, HttpClientError) and (
                    exc.status_code is not None and exc.status_code < 500
                )
                if non_retryable or attempt == self._max_retries:
                    break
                delay = self._backoff_seconds * (2 ** (attempt - 1))
                logger.warning(
                    "%s %s failed (attempt %s/%s), retrying in %.2fs: %s",
                    method,
                    url,
                    attempt,
                    self._max_retries,
                    delay,
                    exc.__class__.__name__,
                )
                await asyncio.sleep(delay)

        status_code = last_error.status_code if isinstance(last_error, HttpClientError) else None
        raise HttpClientError(
            f"Request to {url} failed after {attempts_made} attempt(s): {last_error}",
            status_code=status_code,
        ) from last_error

    async def aclose(self) -> None:
        await self._client.aclose()
