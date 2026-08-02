"""Trusted host middleware setup.

Thin wrapper around Starlette's `TrustedHostMiddleware`, rejecting requests
with a `Host` header outside `settings.allowed_hosts` before they reach
routing. Defaults to `["*"]` in development; lock this down per environment
in `backend/.env` for staging/production.
"""

from __future__ import annotations

from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import Settings


def setup_trusted_hosts(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
