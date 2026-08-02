"""Thin HTTP client wrappers for third-party APIs.

`http_client.py` (`AsyncHttpClient`) provides shared request behavior
(timeouts, retries with backoff, 4xx-vs-5xx error handling) reused by
`search/serper_client.py` and `ai/openrouter_client.py`.
"""
