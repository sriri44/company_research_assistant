"""GZip middleware setup.

Thin wrapper around Starlette's `GZipMiddleware` — compresses responses
above the minimum size threshold (useful once report/opportunity payloads
grow large).
"""

from __future__ import annotations

from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

_MINIMUM_SIZE_BYTES = 1000


def setup_gzip(app: FastAPI) -> None:
    app.add_middleware(GZipMiddleware, minimum_size=_MINIMUM_SIZE_BYTES)
