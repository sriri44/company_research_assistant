"""CompetitorService interface.

Responsibility: given a resolved `Company` (and its AI-derived profile),
identify and rank competitors using `SearchService` + `AIService`.

Out of scope: growth/automation analysis (that's `OpportunityService`) and
report composition (that's `ReportService`).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.company import Company
from app.models.competitor import Competitor


class CompetitorService(ABC):
    @abstractmethod
    async def find_competitors(self, company: Company, limit: int = 5) -> list[Competitor]:
        """Identify and rank competitors for the given company, most
        similar first."""
        raise NotImplementedError
