"""Placeholder ReportService.

Satisfies the `ReportService` interface so the DI graph and API layer are
wireable before the real orchestration implementation exists. See
docs/ROADMAP.md Phase 6.
"""

from __future__ import annotations

from app.models.report import Report
from app.services.interfaces.report_service import ReportService


class PlaceholderReportService(ReportService):
    async def generate_report(self, company_id: str) -> Report:
        raise NotImplementedError(
            "ReportService.generate_report is not implemented yet — see docs/ROADMAP.md"
        )

    async def get_report(self, report_id: str) -> Report:
        raise NotImplementedError(
            "ReportService.get_report is not implemented yet — see docs/ROADMAP.md"
        )
