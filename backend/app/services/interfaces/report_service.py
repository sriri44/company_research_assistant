"""ReportService interface.

Responsibility: the top-level orchestrator. Sequences CompanyService ->
SearchService -> CrawlerService -> AIService -> CompetitorService ->
OpportunityService -> pdf generation, and returns a `Report` aggregate.
This is the only service allowed to know the full pipeline order; every
other service is unaware of its neighbors.

Out of scope: the actual work of any individual stage — this service only
coordinates calls to the other interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.report import Report


class ReportService(ABC):
    @abstractmethod
    async def generate_report(self, company_id: str) -> Report:
        """Run the full research pipeline for a resolved company and
        return the resulting report (status may be `PROCESSING` if the
        pipeline runs asynchronously)."""
        raise NotImplementedError

    @abstractmethod
    async def get_report(self, report_id: str) -> Report:
        """Fetch a report by id, reflecting its current status."""
        raise NotImplementedError
