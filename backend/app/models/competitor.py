"""Domain model: Competitor.

Represents a single competitor identified relative to a resolved `Company`,
as produced by `CompetitorService` / the research pipeline's single AI
analysis call.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Competitor:
    name: str
    domain: str
    similarity_score: float
    summary: str | None = None
    reason: str | None = None
    market_position: str | None = None
