"""Domain model: Report.

The aggregate output produced by `ReportService`, composing the results of
every upstream service into a single deliverable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.models.company import Company
from app.models.competitor import Competitor
from app.models.opportunity import Opportunity


class ReportStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class Report:
    id: str
    company: Company
    status: ReportStatus
    summary: str | None = None
    industry: str | None = None
    phone: str | None = None
    address: str | None = None
    products: list[str] = field(default_factory=list)
    services: list[str] = field(default_factory=list)
    pain_points: list[str] = field(default_factory=list)
    competitors: list[Competitor] = field(default_factory=list)
    opportunities: list[Opportunity] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    confidence: float | None = None
    pdf_url: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None
