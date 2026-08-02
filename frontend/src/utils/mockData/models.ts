// Selectable model catalog for the ModelSelector. There's no backend
// "list models" endpoint (OpenRouter's catalog is huge and changes
// often), so this stays a curated static list — but the `id` values are
// real OpenRouter model slugs, sent as-is in the `model` field of
// POST /api/v1/research (see docs/ROADMAP.md Phase 4/5).

import type { ModelOption } from "@/types/settings";

export const MOCK_MODELS: ModelOption[] = [
  {
    id: "openai/gpt-4o-mini",
    name: "GPT-4o Mini",
    provider: "OpenAI",
    description: "Fast, cost-efficient — best for quick lookups.",
    badge: "fast",
  },
  {
    id: "anthropic/claude-3.5-sonnet",
    name: "Claude 3.5 Sonnet",
    provider: "Anthropic",
    description: "Balanced reasoning and speed for most research tasks.",
    badge: "balanced",
  },
  {
    id: "anthropic/claude-3-opus",
    name: "Claude 3 Opus",
    provider: "Anthropic",
    description: "Deepest analysis for complex, multi-competitor research.",
    badge: "powerful",
  },
  {
    id: "google/gemini-flash-1.5",
    name: "Gemini 1.5 Flash",
    provider: "Google",
    description: "Strong long-context reasoning across large document sets.",
    badge: "balanced",
  },
];

export const DEFAULT_MODEL_ID = MOCK_MODELS[0].id;
