"""Report resource routes — mounted at `/api/v1/report`.

`POST /api/v1/report` and `GET /api/v1/report/{report_id}` remain stubbed
with HTTP 501 until `ReportService` gets a real orchestration
implementation (see docs/ROADMAP.md Phase 6) — the real report-fetching
path today is `GET /api/v1/research/{report_id}` (research_routes.py).

`GET /api/v1/report/{report_id}/pdf` is real: it resolves the same
`ReportService.get_report()` used elsewhere and renders it to a PDF via
`PDFGeneratorService`, unrelated to the still-stubbed create/get pair
above.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.concurrency import run_in_threadpool

from app.api.v1.dependencies.get_pdf_generator_service import get_pdf_generator_service
from app.api.v1.dependencies.get_report_service import get_report_service
from app.pdf.service import PDFGeneratorService
from app.services.interfaces.report_service import ReportService
from app.utils.logger import get_logger

router = APIRouter(prefix="/report", tags=["report"])
logger = get_logger(__name__)


@router.post("")
async def create_report(service: ReportService = Depends(get_report_service)) -> None:
    """Trigger full report generation for a resolved company."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")


@router.get("/{report_id}")
async def get_report(report_id: str, service: ReportService = Depends(get_report_service)) -> None:
    """Fetch a report (and its generation status) by id."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")


@router.get("/{report_id}/pdf")
async def download_report_pdf(
    report_id: str,
    report_service: ReportService = Depends(get_report_service),
    pdf_service: PDFGeneratorService = Depends(get_pdf_generator_service),
) -> Response:
    """Render a completed report to a downloadable PDF.

    Raises (via the global `AppError` handler) `REPORT_NOT_FOUND` (404) if
    `report_id` doesn't exist, or `REPORT_NOT_READY` (409) if the report
    hasn't finished — or failed — generation.
    """
    report = await report_service.get_report(report_id)
    # ReportLab's synchronous rendering is CPU-bound; offload it so it
    # doesn't block the event loop for other in-flight requests.
    pdf_bytes = await run_in_threadpool(pdf_service.generate, report)

    logger.info("PDF generated for report %s (%d bytes)", report_id, len(pdf_bytes))
    filename = f"{report.company.name.strip().replace(' ', '-')}-research-report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
