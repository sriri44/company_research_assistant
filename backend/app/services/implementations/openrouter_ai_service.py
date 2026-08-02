"""OpenRouter-backed AIService implementation.

Loads a prompt template from `app.prompts`, renders it against the given
context, and sends exactly one chat completion request per method call —
`generate_structured` additionally validates the response against the
given Pydantic model, with one local re-parse attempt (stripping markdown
code fences) if the first parse fails. That re-parse is *not* a second AI
call — it's the same response, parsed differently.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from app.ai.openrouter_client import OpenRouterClient
from app.core.exceptions import AIProviderError
from app.services.interfaces.ai_service import AIService
from app.utils.logger import get_logger

logger = get_logger(__name__)

_PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
_SYSTEM_PROMPT = (
    "You are a precise, factual business research analyst. Follow the user's "
    "instructions exactly and return only what is requested — no extra commentary."
)
_JSON_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)


class OpenRouterAIService(AIService):
    def __init__(self, client: OpenRouterClient, default_model: str) -> None:
        self._client = client
        self._default_model = default_model
        self._prompt_cache: dict[str, str] = {}

    async def generate(self, prompt_name: str, context: dict[str, Any]) -> str:
        model, template_context = _split_model_from_context(context, self._default_model)
        user_prompt = self._render(prompt_name, template_context)
        return await self._client.chat_completion(
            model=model,
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            json_response=False,
        )

    async def generate_structured(
        self,
        prompt_name: str,
        context: dict[str, Any],
        response_model: type,
    ) -> Any:
        if not (isinstance(response_model, type) and issubclass(response_model, BaseModel)):
            raise TypeError("generate_structured requires a Pydantic BaseModel subclass")

        model, template_context = _split_model_from_context(context, self._default_model)
        user_prompt = self._render(prompt_name, template_context)

        raw_text = await self._client.chat_completion(
            model=model,
            system_prompt=_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            json_response=True,
        )

        return _parse_structured_response(raw_text, response_model)

    def _render(self, prompt_name: str, context: dict[str, Any]) -> str:
        template = self._prompt_cache.get(prompt_name)
        if template is None:
            path = _PROMPTS_DIR / f"{prompt_name}.prompt.md"
            try:
                template = path.read_text(encoding="utf-8")
            except FileNotFoundError as exc:
                raise AIProviderError(f"Prompt template not found: {prompt_name}") from exc
            self._prompt_cache[prompt_name] = template

        rendered = template
        for key, value in context.items():
            rendered = rendered.replace(f"{{{{{key.upper()}}}}}", str(value))
        return rendered


def _split_model_from_context(
    context: dict[str, Any], default_model: str
) -> tuple[str, dict[str, Any]]:
    """`model` travels through the interface's generic `context` dict —
    `AIService`'s locked signature has no dedicated model parameter — and
    is stripped out here before the remaining keys render the template."""
    model = context.get("model") or default_model
    template_context = {key: value for key, value in context.items() if key != "model"}
    return model, template_context


def _parse_structured_response(raw_text: str, response_model: type[BaseModel]) -> BaseModel:
    candidates = [raw_text, _JSON_FENCE_RE.sub("", raw_text).strip()]

    last_error: Exception | None = None
    for candidate in candidates:
        try:
            return response_model.model_validate_json(candidate)
        except ValidationError as exc:
            last_error = exc
            continue

    logger.warning("AI response failed schema validation: %s", last_error)
    raise AIProviderError(
        "The AI response did not match the expected structured format."
    ) from last_error
