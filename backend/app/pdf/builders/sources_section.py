"""Section 6: Sources — every crawled page and public reference used to
produce this report."""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.report import Report


def build_sources_section(report: Report, styles: StyleSheet1) -> list[Flowable]:
    flowables: list[Flowable] = [Paragraph("Sources", styles["H1"])]

    if not report.sources:
        flowables.append(
            Paragraph("No sources were recorded for this report.", styles["BodyMuted"])
        )
        return flowables

    items = [
        ListItem(Paragraph(source, styles["Bullet"]), leftIndent=6) for source in report.sources
    ]
    flowables.append(
        ListFlowable(items, bulletType="1", start=1, leftIndent=12, bulletFontName="Helvetica")
    )
    return flowables
