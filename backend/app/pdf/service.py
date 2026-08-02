"""PDFGeneratorService — turns a completed `Report` into consulting-style
PDF bytes, ready to stream back as an HTTP response.

Pure rendering boundary: takes an already-built `Report` domain object and
returns bytes. Never fetches, crawls, or calls the AI service itself — see
`app/pdf/__init__.py`. The only thing it needs from outside the report
itself is which AI model the deployment is configured to use (for the
cover page), since `Report` doesn't carry that per-run.
"""

from __future__ import annotations

from io import BytesIO

from reportlab.platypus import PageBreak
from reportlab.platypus.flowables import Flowable

from app.core.exceptions import ReportNotReadyError
from app.models.report import Report, ReportStatus
from app.pdf.builders.competitor_section import build_competitor_section
from app.pdf.builders.cover_section import build_cover_section
from app.pdf.builders.opportunity_section import build_opportunity_section
from app.pdf.builders.pain_points_section import build_pain_points_section
from app.pdf.builders.products_section import build_products_section
from app.pdf.builders.sources_section import build_sources_section
from app.pdf.builders.summary_section import build_summary_section
from app.pdf.builders.toc_section import build_toc_section
from app.pdf.templates.page_template import ReportDocTemplate
from app.pdf.templates.styles import build_stylesheet
from app.utils.time_utils import utcnow


class PDFGeneratorService:
    def __init__(self, *, default_model: str) -> None:
        self._default_model = default_model

    def generate(self, report: Report) -> bytes:
        """Render `report` to PDF bytes. Raises `ReportNotReadyError` if the
        report hasn't finished (or failed) generation."""
        if report.status != ReportStatus.COMPLETE:
            raise ReportNotReadyError(
                f"Report {report.id} is not ready for PDF export (status={report.status.value})."
            )

        styles = build_stylesheet()
        generated_label = utcnow().strftime("%B %d, %Y at %H:%M UTC")

        story: list[Flowable] = []
        story.extend(
            build_cover_section(
                report,
                generated_label=generated_label,
                model_used=self._default_model,
                styles=styles,
            )
        )
        story.extend(build_toc_section(styles))
        story.extend(build_summary_section(report, styles))
        story.append(PageBreak())
        story.extend(build_products_section(report, styles))
        story.append(PageBreak())
        story.extend(build_pain_points_section(report, styles))
        story.append(PageBreak())
        story.extend(build_competitor_section(report, styles))
        story.append(PageBreak())
        story.extend(build_opportunity_section(report, styles))
        story.append(PageBreak())
        story.extend(build_sources_section(report, styles))

        buffer = BytesIO()
        doc = ReportDocTemplate(
            buffer, company_name=report.company.name, generated_label=generated_label
        )
        doc.multiBuild(story)
        return buffer.getvalue()
