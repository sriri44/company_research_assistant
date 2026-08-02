"""Research resource routes — mounted at `/api/v1/research`.

`POST /api/v1/research` is the real entry point to the full pipeline:
resolve company -> search -> crawl -> extract -> one AI call -> map ->
return. `GET /api/v1/research/{report_id}` fetches a previously completed
run from the in-memory report cache. Both delegate everything to
`ResearchReportService` — no business logic lives in this file.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.v1.dependencies.get_research_report_service import get_research_report_service
from app.models.report import Report
from app.schemas.common import SuccessResponse
from app.schemas.research_schema import (
    CompetitorSchema,
    GrowthOpportunitySchema,
    ResearchRequest,
    ResearchResultSchema,
)
from app.services.implementations.research_report_service import ResearchReportService
from app.utils.response_helper import build_success_response

router = APIRouter(prefix="/research", tags=["research"])


@router.post("", response_model=SuccessResponse[ResearchResultSchema])
async def create_research(
    payload: ResearchRequest,
    service: ResearchReportService = Depends(get_research_report_service),
) -> SuccessResponse[ResearchResultSchema]:
    """Run the full research pipeline for a company name or website."""
    report = await service.run_research(payload.query, payload.model)
    return build_success_response(_to_research_result(report))


@router.get("/{report_id}", response_model=SuccessResponse[ResearchResultSchema])
async def get_research(
    report_id: str,
    service: ResearchReportService = Depends(get_research_report_service),
) -> SuccessResponse[ResearchResultSchema]:
    """Fetch a previously completed (or failed) research run by id."""
    report = await service.get_report(report_id)
    return build_success_response(_to_research_result(report))


def _to_research_result(report: Report) -> ResearchResultSchema:
    return ResearchResultSchema(
        report_id=report.id,
        status=report.status.value,
        company_name=report.company.name,
        website=report.company.domain,
        phone=report.phone,
        address=report.address,
        summary=report.summary,
        industry=report.industry,
        products=report.products,
        services=report.services,
        pain_points=report.pain_points,
        competitors=[
            CompetitorSchema(
                name=competitor.name,
                website=competitor.domain,
                reason=competitor.reason,
                market_position=competitor.market_position,
            )
            for competitor in report.competitors
        ],
        growth_opportunities=[
            GrowthOpportunitySchema(
                title=opportunity.title,
                description=opportunity.description,
                business_impact=opportunity.impact.value,
                implementation_complexity=opportunity.complexity.value,
                priority_score=opportunity.priority_score,
                estimated_roi=opportunity.estimated_roi,
            )
            for opportunity in report.opportunities
        ],
        sources=report.sources,
        confidence=report.confidence,
    )
