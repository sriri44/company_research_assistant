"""Section 1: Executive Summary — company overview, industry, and the
AI-generated business description."""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.report import Report
from app.pdf import theme


def _fact_row(label: str, value: str, styles: StyleSheet1) -> list[Paragraph]:
    return [Paragraph(label, styles["TableCell"]), Paragraph(value, styles["TableCell"])]


def build_summary_section(report: Report, styles: StyleSheet1) -> list[Flowable]:
    company = report.company
    flowables: list[Flowable] = [Paragraph("Executive Summary", styles["H1"])]

    flowables.append(Paragraph("Company Overview", styles["H2"]))
    facts: list[list[Paragraph]] = [_fact_row("Website", company.domain, styles)]
    if report.industry:
        facts.append(_fact_row("Industry", report.industry, styles))
    if report.phone:
        facts.append(_fact_row("Phone", report.phone, styles))
    if report.address:
        facts.append(_fact_row("Address", report.address, styles))

    facts_table = Table(facts, colWidths=[110, 330], hAlign="LEFT")
    facts_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, theme.SLATE_100),
                ("FONTNAME", (0, 0), (0, -1), theme.FONT_BOLD),
                ("TEXTCOLOR", (0, 0), (0, -1), theme.SLATE_500),
            ]
        )
    )
    flowables.append(facts_table)
    flowables.append(Spacer(1, 12))

    flowables.append(Paragraph("Business Description", styles["H2"]))
    description = report.summary or "No business description could be generated for this company."
    flowables.append(Paragraph(description, styles["Body"]))

    return flowables
