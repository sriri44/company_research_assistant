"""Placeholder CompetitorService.

Satisfies the `CompetitorService` interface so the DI graph and API layer
are wireable before a real implementation exists. See docs/ROADMAP.md
Phase 4.
"""

from __future__ import annotations

from app.models.company import Company
from app.models.competitor import Competitor
from app.services.interfaces.competitor_service import CompetitorService


class PlaceholderCompetitorService(CompetitorService):
    async def find_competitors(self, company: Company, limit: int = 5) -> list[Competitor]:
        raise NotImplementedError(
            "CompetitorService.find_competitors is not implemented yet — see docs/ROADMAP.md"
        )
