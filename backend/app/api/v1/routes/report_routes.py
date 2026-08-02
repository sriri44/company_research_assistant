"""Report resource routes — mounted at `/api/v1/report`.

Stubbed with HTTP 501 until `ReportService` gets a real orchestration
implementation (see docs/ROADMAP.md Phase 6). Each handler still resolves
a real `ReportService` instance via `Depends()`, it just never calls it.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies.get_report_service import get_report_service
from app.services.interfaces.report_service import ReportService

router = APIRouter(prefix="/report", tags=["report"])


@router.post("")
async def create_report(service: ReportService = Depends(get_report_service)) -> None:
    """Trigger full report generation for a resolved company."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")


@router.get("/{report_id}")
async def get_report(report_id: str, service: ReportService = Depends(get_report_service)) -> None:
    """Fetch a report (and its generation status) by id."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")
