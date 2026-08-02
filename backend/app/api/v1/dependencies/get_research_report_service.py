"""FastAPI dependency provider for the concrete `ResearchReportService`.

Separate from `get_report_service` (which returns the `ReportService`
interface type) because `research_routes.py` needs `run_research(query,
model)` — a method beyond the locked `ReportService` ABC, added on the
concrete class rather than by changing the interface.
"""

from __future__ import annotations

from app.core.container import get_container
from app.services.implementations.research_report_service import ResearchReportService


def get_research_report_service() -> ResearchReportService:
    return get_container().research_report_service
