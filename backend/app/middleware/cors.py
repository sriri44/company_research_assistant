"""CORS middleware setup.

Thin wrapper around Starlette's `CORSMiddleware` so `app.main` doesn't
need to know the allowed-origins policy — it just calls `setup_cors`.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings


def setup_cors(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Content-Disposition isn't in the CORS "simple response headers"
        # allowlist, so without this the PDF download's real filename
        # (report_routes.download_report_pdf) is invisible to frontend JS
        # across the Netlify/Render origin split — it silently falls back
        # to a generic name instead of erroring, which makes it easy to miss.
        expose_headers=["Content-Disposition"],
    )
