"""AIService interface.

Responsibility: send normalized content + a named prompt template to an AI
model (via OpenRouter) and return structured output. Generic — reused by
company summarization, competitor analysis, and (indirectly, through its
own engine) AI Growth Opportunities(tm).

Out of scope: authoring prompt content (lives in `app.prompts`) and
domain-specific interpretation of the result (that belongs to the calling
service, e.g. `CompetitorService`, `app.ai.opportunities`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIService(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt_name: str,
        context: dict[str, Any],
    ) -> str:
        """Render the named prompt template with `context` and return the
        raw model completion as text."""
        raise NotImplementedError

    @abstractmethod
    async def generate_structured(
        self,
        prompt_name: str,
        context: dict[str, Any],
        response_model: type,
    ) -> Any:
        """Render the named prompt template and parse the model output into
        `response_model` (e.g., a Pydantic model), raising a domain
        exception if parsing/validation fails."""
        raise NotImplementedError
