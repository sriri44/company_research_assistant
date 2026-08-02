"""Integration tests for GET /api/v1/report/{report_id}/pdf.

Same fake-service-via-dependency-override pattern as
test_research_endpoint.py — `get_report_service` is swapped so no real
research pipeline runs; only the PDF rendering path is exercised.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies.get_report_service import get_report_service
from app.core.exceptions import ReportNotFoundError
from app.main import app
from app.models.company import Company
from app.models.competitor import Competitor
from app.models.opportunity import ComplexityLevel, ImpactLevel, Opportunity
from app.models.report import Report, ReportStatus


def _sample_report(status: ReportStatus = ReportStatus.COMPLETE) -> Report:
    company = Company(
        id="c1", name="Acme Corp", domain="acme.com", resolved_at=datetime.now(timezone.utc)
    )
    return Report(
        id="r1",
        company=company,
        status=status,
        summary="Acme makes widgets.",
        industry="Manufacturing",
        products=["Widgets"],
        services=["Widget repair"],
        pain_points=["Manual order processing", "Critical compliance risk in shipping"],
        competitors=[
            Competitor(
                name="Widgets Inc",
                domain="widgetsinc.com",
                similarity_score=0.9,
                reason="Direct competitor",
                market_position="Leader",
            )
        ],
        opportunities=[
            Opportunity(
                title="Automate order intake",
                description="Use AI to parse incoming orders.",
                category="AI Growth Opportunity",
                impact=ImpactLevel.HIGH,
                complexity=ComplexityLevel.MEDIUM,
                priority_score=88,
                estimated_roi="20% faster processing",
            )
        ],
        sources=["https://acme.com"],
        confidence=0.8,
        completed_at=datetime.now(timezone.utc),
    )


class _FakeReportService:
    def __init__(self, report: Report | None = None) -> None:
        self._report = report

    async def generate_report(self, company_id: str) -> Report:
        raise NotImplementedError

    async def get_report(self, report_id: str) -> Report:
        if self._report is None or report_id != self._report.id:
            raise ReportNotFoundError(f"No report found for id={report_id}")
        return self._report


@pytest.fixture(autouse=True)
def _reset_overrides() -> Iterator[None]:
    yield
    app.dependency_overrides.pop(get_report_service, None)


def test_download_pdf_for_complete_report_returns_pdf_bytes(client: TestClient) -> None:
    report = _sample_report()
    app.dependency_overrides[get_report_service] = lambda: _FakeReportService(report)

    response = client.get(f"/api/v1/report/{report.id}/pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 1000


def test_download_pdf_exposes_content_disposition_cross_origin(client: TestClient) -> None:
    """Regression test: without `expose_headers=["Content-Disposition"]` on
    CORSMiddleware, the browser can receive the header over the wire but
    JS can't read it — the frontend's real filename silently falls back to
    a generic one instead of erroring, which makes the bug easy to miss."""
    report = _sample_report()
    app.dependency_overrides[get_report_service] = lambda: _FakeReportService(report)

    response = client.get(
        f"/api/v1/report/{report.id}/pdf", headers={"Origin": "http://localhost:5173"}
    )

    assert response.status_code == 200
    exposed = response.headers.get("access-control-expose-headers", "")
    assert "Content-Disposition" in exposed


def test_download_pdf_returns_404_for_unknown_report(client: TestClient) -> None:
    app.dependency_overrides[get_report_service] = lambda: _FakeReportService(None)

    response = client.get("/api/v1/report/does-not-exist/pdf")

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "REPORT_NOT_FOUND"


@pytest.mark.parametrize(
    "status_value", [ReportStatus.PROCESSING, ReportStatus.QUEUED, ReportStatus.FAILED]
)
def test_download_pdf_returns_409_when_report_not_ready(
    client: TestClient, status_value: ReportStatus
) -> None:
    report = _sample_report(status=status_value)
    app.dependency_overrides[get_report_service] = lambda: _FakeReportService(report)

    response = client.get(f"/api/v1/report/{report.id}/pdf")

    assert response.status_code == 409
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "REPORT_NOT_READY"


def test_download_pdf_handles_report_with_no_optional_data(client: TestClient) -> None:
    company = Company(id="c2", name="Sparse Co", domain="sparse.example")
    report = Report(id="r2", company=company, status=ReportStatus.COMPLETE)
    app.dependency_overrides[get_report_service] = lambda: _FakeReportService(report)

    response = client.get(f"/api/v1/report/{report.id}/pdf")

    assert response.status_code == 200
    assert response.content.startswith(b"%PDF")
