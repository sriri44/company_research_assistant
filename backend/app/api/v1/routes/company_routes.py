"""Company resource routes — mounted at `/api/v1/company`.

Stubbed with HTTP 501 until `CompanyService` gets a real implementation
(see docs/ROADMAP.md Phase 2). Present now so the URL surface and DI
wiring exist ahead of behavior — each handler still resolves a real
`CompanyService` instance via `Depends()`, it just never calls it.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies.get_company_service import get_company_service
from app.services.interfaces.company_service import CompanyService

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/resolve")
async def resolve_company(service: CompanyService = Depends(get_company_service)) -> None:
    """Resolve a company name or URL into a canonical identity."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")


@router.get("/{company_id}")
async def get_company(
    company_id: str, service: CompanyService = Depends(get_company_service)
) -> None:
    """Fetch a previously resolved company by id."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")
