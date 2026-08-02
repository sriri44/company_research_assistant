"""Report-facing schemas.

`JobStatus` models the state of a long-running report generation job (see
`app.models.report.ReportStatus`); populated by `ReportService`'s real
implementation starting Phase 6. Schema only — no report request/response
DTOs yet, since `report_routes.py` is still a 501 stub in this phase.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class JobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "complete", "failed"]
    progress: float | None = None
    message: str | None = None
