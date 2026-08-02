"""Placeholder AIService.

Satisfies the `AIService` interface so the DI graph and API layer are
wireable before a real OpenRouter-backed implementation exists. See
docs/ROADMAP.md Phase 3.
"""

from __future__ import annotations

from typing import Any

from app.services.interfaces.ai_service import AIService


class PlaceholderAIService(AIService):
    async def generate(self, prompt_name: str, context: dict[str, Any]) -> str:
        raise NotImplementedError("AIService.generate is not implemented yet — see docs/ROADMAP.md")

    async def generate_structured(
        self,
        prompt_name: str,
        context: dict[str, Any],
        response_model: type,
    ) -> Any:
        raise NotImplementedError(
            "AIService.generate_structured is not implemented yet — see docs/ROADMAP.md"
        )
