"""Section 2: Products & Services."""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import ListFlowable, ListItem, Spacer
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.models.report import Report


def _bullet_list(items: list[str], styles: StyleSheet1) -> Flowable:
    return ListFlowable(
        [ListItem(Paragraph(item, styles["Bullet"]), leftIndent=6) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=12,
    )


def build_products_section(report: Report, styles: StyleSheet1) -> list[Flowable]:
    flowables: list[Flowable] = [Paragraph("Products &amp; Services", styles["H1"])]

    flowables.append(Paragraph("Products", styles["H2"]))
    if report.products:
        flowables.append(_bullet_list(report.products, styles))
    else:
        flowables.append(Paragraph("No specific products were identified.", styles["BodyMuted"]))
    flowables.append(Spacer(1, 10))

    flowables.append(Paragraph("Services", styles["H2"]))
    if report.services:
        flowables.append(_bullet_list(report.services, styles))
    else:
        flowables.append(Paragraph("No specific services were identified.", styles["BodyMuted"]))

    return flowables
