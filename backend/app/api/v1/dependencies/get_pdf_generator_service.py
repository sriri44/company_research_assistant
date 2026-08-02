"""FastAPI dependency provider for `PDFGeneratorService`.

Stateless and config-only (no shared HTTP client / crawler / AI resources),
so it's constructed directly here rather than through `app.core.container`
— it never needs to be swapped or mocked across environments the way the
research pipeline's providers do.
"""

from __future__ import annotations

from functools import lru_cache

from app.core.config import get_settings
from app.pdf.service import PDFGeneratorService


@lru_cache
def get_pdf_generator_service() -> PDFGeneratorService:
    settings = get_settings()
    return PDFGeneratorService(default_model=settings.openrouter_default_model)
