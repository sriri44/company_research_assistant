"""Maps `ResearchAnalysisResult` (the AI's structured output) to domain
objects. Shared by `ResearchReportService`, `AICompetitorService`, and
`AIOpportunityService` so this mapping logic exists in exactly one place.
"""

from __future__ import annotations

from urllib.parse import urlparse

from app.ai.schemas import AICompetitor, AIOpportunity
from app.models.competitor import Competitor
from app.models.opportunity import ComplexityLevel, ImpactLevel, Opportunity

_DEFAULT_OPPORTUNITY_CATEGORY = "AI Growth Opportunity"


def to_competitor(item: AICompetitor, *, rank: int) -> Competitor:
    """`rank` (0-indexed, in the AI's own priority order) drives a simple
    descending `similarity_score` since the AI schema doesn't return one
    explicitly — first-listed competitors are treated as most similar."""
    domain = _domain_from_website(item.website) or item.name.lower().replace(" ", "")
    return Competitor(
        name=item.name,
        domain=domain,
        similarity_score=round(max(0.3, 1.0 - rank * 0.15), 2),
        summary=item.reason,
        reason=item.reason,
        market_position=item.market_position,
    )


def to_opportunity(item: AIOpportunity) -> Opportunity:
    return Opportunity(
        title=item.title,
        description=item.description,
        category=_DEFAULT_OPPORTUNITY_CATEGORY,
        impact=ImpactLevel(item.business_impact),
        complexity=ComplexityLevel(item.implementation_complexity),
        priority_score=item.priority_score,
        estimated_roi=item.estimated_roi,
    )


def _domain_from_website(website: str | None) -> str | None:
    if not website:
        return None
    candidate = website if website.startswith(("http://", "https://")) else f"https://{website}"
    netloc = urlparse(candidate).netloc
    if not netloc:
        return None
    return netloc[4:] if netloc.startswith("www.") else netloc
