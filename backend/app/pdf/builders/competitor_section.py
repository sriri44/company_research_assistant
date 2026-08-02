"""Section 4: Competitor Analysis — Company / Website / Reason / Market
Position table."""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.report import Report
from app.pdf import theme


def build_competitor_section(report: Report, styles: StyleSheet1) -> list[Flowable]:
    flowables: list[Flowable] = [Paragraph("Competitor Analysis", styles["H1"])]

    if not report.competitors:
        flowables.append(
            Paragraph("No competitors were identified for this company.", styles["BodyMuted"])
        )
        return flowables

    header = [
        Paragraph("Company", styles["TableHeader"]),
        Paragraph("Website", styles["TableHeader"]),
        Paragraph("Reason", styles["TableHeader"]),
        Paragraph("Market Position", styles["TableHeader"]),
    ]
    rows: list[list[Paragraph]] = [header]
    for competitor in report.competitors:
        rows.append(
            [
                Paragraph(competitor.name, styles["TableCell"]),
                Paragraph(competitor.domain, styles["TableCell"]),
                Paragraph(competitor.reason or "—", styles["TableCell"]),
                Paragraph(competitor.market_position or "—", styles["TableCell"]),
            ]
        )

    table = Table(rows, colWidths=[95, 95, 165, 100], repeatRows=1, hAlign="LEFT")
    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), theme.PRIMARY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, theme.SLATE_100),
        ("GRID", (0, 0), (-1, 0), 0, theme.PRIMARY),
    ]
    for row_index in range(1, len(rows)):
        if row_index % 2 == 0:
            style_commands.append(("BACKGROUND", (0, row_index), (-1, row_index), theme.SLATE_50))
    table.setStyle(TableStyle(style_commands))

    flowables.append(table)
    return flowables
