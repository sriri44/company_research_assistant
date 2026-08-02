"""Section 3: Pain Points — bullet list with severity badges.

`Report.pain_points` is a plain list of strings (no severity field on the
domain model — nothing upstream changed to add one). Severity is inferred
here, in the presentation layer only, via a simple keyword heuristic so
the report reads like a consulting deliverable instead of a flat list.
This never touches the AI pipeline or its output.
"""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.report import Report
from app.pdf import theme

_HIGH_KEYWORDS = (
    "critical", "compliance", "security", "risk", "regulat", "fraud",
    "outage", "downtime", "breach", "penalt", "legal",
)
_LOW_KEYWORDS = ("minor", "occasional", "cosmetic", "nice to have")


def _infer_severity(text: str) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in _HIGH_KEYWORDS):
        return "high"
    if any(keyword in lowered for keyword in _LOW_KEYWORDS):
        return "low"
    return "medium"


def _badge(severity: str, styles: StyleSheet1) -> Table:
    text_color, bg_color = theme.SEVERITY_COLORS[severity]
    style = styles["CardMeta"].clone(f"Badge{severity}", textColor=text_color)
    cell = Table([[Paragraph(severity.upper(), style)]], colWidths=[52])
    cell.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg_color),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return cell


def build_pain_points_section(report: Report, styles: StyleSheet1) -> list[Flowable]:
    flowables: list[Flowable] = [Paragraph("Pain Points", styles["H1"])]

    if not report.pain_points:
        flowables.append(
            Paragraph("No significant pain points were identified.", styles["BodyMuted"])
        )
        return flowables

    rows = [
        [_badge(_infer_severity(point), styles), Paragraph(point, styles["Body"])]
        for point in report.pain_points
    ]
    table = Table(rows, colWidths=[60, 380], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, theme.SLATE_100),
            ]
        )
    )
    flowables.append(table)
    flowables.append(Spacer(1, 4))
    return flowables
