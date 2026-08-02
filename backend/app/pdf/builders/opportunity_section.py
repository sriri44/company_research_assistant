"""Section 5: AI Growth Opportunities(tm) — professional cards with title,
description, impact/complexity badges, priority score, and estimated ROI.
"""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import KeepTogether, Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.opportunity import Opportunity
from app.models.report import Report
from app.pdf import theme

_PILL_H_PADDING = 8


def _pill(label: str, severity: str, styles: StyleSheet1) -> Table:
    text_color, bg_color = theme.SEVERITY_COLORS[severity]
    style = styles["CardMeta"].clone(f"Pill{label}{severity}", textColor=text_color)
    # Table.wrap() stretches an unbound column to fill whatever width its
    # parent offers rather than shrinking to content, so a badge needs an
    # explicit content-measured colWidth or it stretches edge-to-edge.
    text_width = stringWidth(label, style.fontName, style.fontSize)
    cell = Table([[Paragraph(label, style)]], colWidths=[text_width + 2 * _PILL_H_PADDING])
    cell.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), _PILL_H_PADDING),
                ("RIGHTPADDING", (0, 0), (-1, -1), _PILL_H_PADDING),
            ]
        )
    )
    return cell


def _opportunity_card(opportunity: Opportunity, index: int, styles: StyleSheet1) -> Flowable:
    header_row = Table(
        [
            [
                Paragraph(f"{index}. {opportunity.title}", styles["CardTitle"]),
                Paragraph(f"Priority {opportunity.priority_score:.0f}/100", styles["CardMeta"]),
            ]
        ],
        colWidths=[350, 100],
    )
    header_row.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TEXTCOLOR", (1, 0), (1, 0), theme.PRIMARY),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    meta_cells = [
        _pill(f"{opportunity.impact.value.upper()} IMPACT", opportunity.impact.value, styles),
        _pill(
            f"{opportunity.complexity.value.upper()} COMPLEXITY",
            opportunity.complexity.value,
            styles,
        ),
    ]
    meta_row = Table([meta_cells], hAlign="LEFT")
    meta_row.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("LEFTPADDING", (1, 0), (1, 0), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    body: list[Flowable] = [
        header_row,
        Spacer(1, 6),
        Paragraph(opportunity.description, styles["CardBody"]),
        Spacer(1, 8),
        meta_row,
    ]
    if opportunity.estimated_roi:
        body.append(Spacer(1, 6))
        body.append(Paragraph(f"Estimated ROI: {opportunity.estimated_roi}", styles["CardMeta"]))

    card = Table([[body]], colWidths=[450])
    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), theme.SLATE_50),
                ("BOX", (0, 0), (-1, -1), 0.75, theme.SLATE_300),
                ("LINEBEFORE", (0, 0), (0, 0), 3, theme.PRIMARY),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ]
        )
    )
    return KeepTogether([card, Spacer(1, 12)])


def build_opportunity_section(report: Report, styles: StyleSheet1) -> list[Flowable]:
    flowables: list[Flowable] = [Paragraph("AI Growth Opportunities™", styles["H1"])]

    if not report.opportunities:
        flowables.append(
            Paragraph(
                "No growth opportunities were identified for this company.",
                styles["BodyMuted"],
            )
        )
        return flowables

    for index, opportunity in enumerate(report.opportunities, start=1):
        flowables.append(_opportunity_card(opportunity, index, styles))

    return flowables
