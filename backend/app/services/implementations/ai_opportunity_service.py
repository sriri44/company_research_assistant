"""AI-backed OpportunityService implementation — AI Growth Opportunities™.

Used when `generate_opportunities` is invoked standalone (outside the main
`/api/v1/research` pipeline, which derives opportunities from its own
single combined AI analysis call instead — see `research_report_service.py`).
Reuses the same `research_analysis` prompt/schema rather than a bespoke
opportunities-only prompt, so prompt-engineering logic lives in exactly
one place; only the `growth_opportunities` slice of the result is used
here.
"""

from __future__ import annotations

from app.ai.mappers import to_opportunity
from app.ai.schemas import ResearchAnalysisResult
from app.models.company import Company
from app.models.opportunity import Opportunity
from app.services.interfaces.ai_service import AIService
from app.services.interfaces.opportunity_service import OpportunityService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AIOpportunityService(OpportunityService):
    def __init__(self, ai_service: AIService) -> None:
        self._ai_service = ai_service

    async def generate_opportunities(self, company: Company) -> list[Opportunity]:
        result = await self._ai_service.generate_structured(
            "research_analysis",
            {
                "company_name": company.name,
                "website": company.domain,
                "context": f"(no crawled content available for this standalone lookup — "
                f"company: {company.name}, {company.domain})",
                "competitor_hints": "(not applicable for this standalone lookup)",
            },
            ResearchAnalysisResult,
        )

        opportunities = [to_opportunity(item) for item in result.growth_opportunities]
        return sorted(opportunities, key=lambda item: item.priority_score, reverse=True)
