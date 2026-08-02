"""OpportunityService interface — AI Growth Opportunities(tm).

Responsibility: given a resolved `Company` and its AI-derived profile,
produce a ranked list of automation/growth opportunities, each scored for
estimated business impact, implementation complexity, and an overall
priority score.

Implementation lives behind `app.ai.opportunities` (the dedicated engine
module for this flagship feature); this interface is the only way the rest
of the backend is allowed to reach it.

Out of scope: competitor analysis, report/PDF composition.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.company import Company
from app.models.opportunity import Opportunity


class OpportunityService(ABC):
    @abstractmethod
    async def generate_opportunities(self, company: Company) -> list[Opportunity]:
        """Generate ranked AI Growth Opportunities(tm) for the given
        company, highest priority first."""
        raise NotImplementedError
