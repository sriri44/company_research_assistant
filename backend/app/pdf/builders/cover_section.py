"""Cover page section: report title, company identity, and generation
metadata over the full-bleed brand-colored background painted by
`ReportDocTemplate._draw_cover_page`.

No image logo fetching happens here — `Company`/`Report` carry no logo URL
today, and this module only renders data it's handed (per the "PDF
generation only" scope of this feature). When no logo is available, a
monogram badge (the company's first initial) stands in as the professional
placeholder branding element instead of leaving dead space.
"""

from __future__ import annotations

from reportlab.graphics.shapes import Circle, Drawing, String
from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import NextPageTemplate, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.report import Report
from app.pdf import theme


def _monogram(letter: str) -> Drawing:
    size = 64
    drawing = Drawing(size, size)
    drawing.add(Circle(size / 2, size / 2, size / 2, fillColor=theme.WHITE, strokeColor=None))
    drawing.add(
        String(
            size / 2,
            size / 2 - 10,
            letter,
            fontName=theme.FONT_BOLD,
            fontSize=28,
            fillColor=theme.PRIMARY_DARK,
            textAnchor="middle",
        )
    )
    return drawing


def _meta_row(label: str, value: str, styles: StyleSheet1) -> list[Paragraph]:
    return [
        Paragraph(label.upper(), styles["CoverMetaLabel"]),
        Paragraph(value, styles["CoverMetaValue"]),
    ]


def build_cover_section(
    report: Report, *, generated_label: str, model_used: str, styles: StyleSheet1
) -> list[Flowable]:
    company = report.company
    initial = (company.name or "?").strip()[:1].upper() or "?"
    confidence_pct = (
        f"{round(report.confidence * 100)}%" if report.confidence is not None else "N/A"
    )

    flowables: list[Flowable] = [
        _monogram(initial),
        Spacer(1, 22),
        Paragraph("AI COMPANY RESEARCH REPORT", styles["CoverSubtitle"]),
        Spacer(1, 6),
        Paragraph(company.name, styles["CoverTitle"]),
        Spacer(1, 4),
        Paragraph(company.domain, styles["CoverSubtitle"]),
        Spacer(1, 48),
    ]

    meta_table = Table(
        [
            _meta_row("Generated", generated_label, styles),
            _meta_row("AI Model Used", model_used, styles),
            _meta_row("Confidence Score", confidence_pct, styles),
        ],
        colWidths=[140, 260],
        hAlign="LEFT",
    )
    meta_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    flowables.append(meta_table)
    flowables.append(NextPageTemplate("Content"))

    return flowables
