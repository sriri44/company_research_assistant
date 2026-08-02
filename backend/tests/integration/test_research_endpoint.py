"""Integration tests for POST/GET /api/v1/research — the real
ResearchReportService is swapped out via FastAPI dependency overrides so
no real Serper/OpenRouter/Crawl4AI calls happen (external APIs mocked at
the service boundary).
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.api.v1.dependencies.get_research_report_service import get_research_report_service
from app.core.exceptions import CompanyNotFoundError, ReportNotFoundError
from app.main import app
from app.models.company import Company
from app.models.competitor import Competitor
from app.models.opportunity import ComplexityLevel, ImpactLevel, Opportunity
from app.models.report import Report, ReportStatus


def _sample_report() -> Report:
    company = Company(
        id="c1", name="Acme Corp", domain="acme.com", resolved_at=datetime.now(timezone.utc)
    )
    return Report(
        id="r1",
        company=company,
        status=ReportStatus.COMPLETE,
        summary="Acme makes widgets.",
        industry="Manufacturing",
        products=["Widgets"],
        services=[],
        pain_points=["Manual order processing"],
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
    )


class _FakeResearchReportService:
    def __init__(self, report: Report | None = None, error: Exception | None = None) -> None:
        self._report = report
        self._error = error

    async def run_research(self, query: str, model: str | None = None) -> Report:
        if self._error:
            raise self._error
        assert self._report is not None
        return self._report

    async def get_report(self, report_id: str) -> Report:
        if self._report is None or report_id != self._report.id:
            raise ReportNotFoundError(f"No report found for id={report_id}")
        return self._report


@pytest.fixture(autouse=True)
def _reset_overrides() -> Iterator[None]:
    yield
    app.dependency_overrides.pop(get_research_report_service, None)


def test_post_research_returns_structured_result(client: TestClient) -> None:
    report = _sample_report()
    app.dependency_overrides[get_research_report_service] = lambda: _FakeResearchReportService(
        report
    )

    response = client.post("/api/v1/research", json={"query": "Acme Corp"})

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["company_name"] == "Acme Corp"
    assert data["website"] == "acme.com"
    assert data["status"] == "complete"
    assert len(data["competitors"]) == 1
    assert data["competitors"][0]["name"] == "Widgets Inc"
    assert len(data["growth_opportunities"]) == 1
    assert data["growth_opportunities"][0]["priority_score"] == 88
    assert data["confidence"] == 0.8


def test_post_research_requires_non_empty_query(client: TestClient) -> None:
    response = client.post("/api/v1/research", json={"query": ""})

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_post_research_returns_404_when_company_cannot_be_resolved(client: TestClient) -> None:
    app.dependency_overrides[get_research_report_service] = lambda: _FakeResearchReportService(
        error=CompanyNotFoundError("Could not resolve an official website.")
    )

    response = client.post("/api/v1/research", json={"query": "zzz-not-a-real-company-zzz"})

    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "COMPANY_NOT_FOUND"


def test_get_research_returns_previously_completed_report(client: TestClient) -> None:
    report = _sample_report()
    app.dependency_overrides[get_research_report_service] = lambda: _FakeResearchReportService(
        report
    )

    response = client.get(f"/api/v1/research/{report.id}")

    assert response.status_code == 200
    assert response.json()["data"]["report_id"] == report.id


def test_get_research_returns_404_for_unknown_id(client: TestClient) -> None:
    app.dependency_overrides[get_research_report_service] = lambda: _FakeResearchReportService(None)

    response = client.get("/api/v1/research/does-not-exist")

    assert response.status_code == 404


def test_unhandled_exception_still_carries_cors_headers() -> None:
    """Regression test: Starlette routes bare-`Exception` handlers through
    `ServerErrorMiddleware`, which sits outside `CORSMiddleware` — without
    the fix in `error_handler._attach_cors_headers`, an unexpected bug
    would look like a CORS failure in the browser instead of the real
    error. A plain `RuntimeError` (not an `AppError`) exercises that path.

    Uses `raise_server_exceptions=False` (unlike the shared `client`
    fixture) so the TestClient returns the real 500 response instead of
    re-raising the exception into the test — matching what an actual
    browser/HTTP client sees in production."""
    app.dependency_overrides[get_research_report_service] = lambda: _FakeResearchReportService(
        error=RuntimeError("boom — simulates an unexpected, unhandled failure")
    )
    allowed_origin = "http://localhost:5173"

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post(
            "/api/v1/research",
            json={"query": "stripe.com"},
            headers={"Origin": allowed_origin},
        )

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert response.headers.get("access-control-allow-origin") == allowed_origin


def test_unhandled_exception_does_not_leak_cors_for_disallowed_origin() -> None:
    app.dependency_overrides[get_research_report_service] = lambda: _FakeResearchReportService(
        error=RuntimeError("boom")
    )

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.post(
            "/api/v1/research",
            json={"query": "stripe.com"},
            headers={"Origin": "https://not-an-allowed-origin.example.com"},
        )

    assert response.status_code == 500
    assert "access-control-allow-origin" not in response.headers
