"""Opportunity resource routes — mounted at `/api/v1/opportunities`.

Backs the flagship AI Growth Opportunities(tm) feature. Stubbed with HTTP
501 until `OpportunityService` gets a real implementation backed by
`app.ai.opportunities` (see docs/ROADMAP.md Phase 5). The handler still
resolves a real `OpportunityService` instance via `Depends()`, it just
never calls it.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies.get_opportunity_service import get_opportunity_service
from app.services.interfaces.opportunity_service import OpportunityService

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("/{company_id}")
async def get_opportunities(
    company_id: str,
    service: OpportunityService = Depends(get_opportunity_service),
) -> None:
    """Fetch ranked AI Growth Opportunities(tm) for a resolved company."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")
