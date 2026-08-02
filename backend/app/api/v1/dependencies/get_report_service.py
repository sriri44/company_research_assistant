"""FastAPI dependency provider for `ReportService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.report_service import ReportService


def get_report_service() -> ReportService:
    return get_container().report_service
