"""AI + Serper-backed CompetitorService implementation.

Used when `find_competitors` is invoked standalone (outside the main
`/api/v1/research` pipeline, which derives competitors from its own single
combined AI analysis call instead — see `research_report_service.py` for
why that path never calls this service, to keep to exactly one AI call
per research run). Reuses the same `research_analysis` prompt/schema
rather than a bespoke competitor-only prompt, so prompt-engineering logic
lives in exactly one place; only the `competitors` slice of the result is
used here. Grounds the AI in real Serper search results so it isn't
reasoning from nothing.
"""

from __future__ import annotations

from app.ai.mappers import to_competitor
from app.ai.schemas import ResearchAnalysisResult
from app.models.company import Company
from app.models.competitor import Competitor
from app.services.interfaces.ai_service import AIService
from app.services.interfaces.competitor_service import CompetitorService
from app.services.interfaces.search_service import SearchService
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AICompetitorService(CompetitorService):
    def __init__(self, search_service: SearchService, ai_service: AIService) -> None:
        self._search_service = search_service
        self._ai_service = ai_service

    async def find_competitors(self, company: Company, limit: int = 5) -> list[Competitor]:
        candidate_urls = await self._search_service.search_company(company, limit=10)
        hints = "\n".join(f"- {url}" for url in candidate_urls) or "(no search results found)"

        result = await self._ai_service.generate_structured(
            "research_analysis",
            {
                "company_name": company.name,
                "website": company.domain,
                "context": f"(no crawled content available for this standalone lookup — "
                f"company: {company.name}, {company.domain})",
                "competitor_hints": hints,
            },
            ResearchAnalysisResult,
        )

        competitors = [
            to_competitor(item, rank=rank) for rank, item in enumerate(result.competitors)
        ]
        return competitors[:limit]
