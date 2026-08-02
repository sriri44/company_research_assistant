"""Placeholder OpportunityService (AI Growth Opportunities(tm)).

Satisfies the `OpportunityService` interface so the DI graph and API layer
are wireable before the real `app.ai.opportunities` engine exists. See
docs/ROADMAP.md Phase 5.
"""

from __future__ import annotations

from app.models.company import Company
from app.models.opportunity import Opportunity
from app.services.interfaces.opportunity_service import OpportunityService


class PlaceholderOpportunityService(OpportunityService):
    async def generate_opportunities(self, company: Company) -> list[Opportunity]:
        raise NotImplementedError(
            "OpportunityService.generate_opportunities is not implemented yet — see docs/ROADMAP.md"
        )
