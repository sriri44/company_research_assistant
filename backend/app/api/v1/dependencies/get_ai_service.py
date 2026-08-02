"""FastAPI dependency provider for `AIService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.ai_service import AIService


def get_ai_service() -> AIService:
    return get_container().ai_service
