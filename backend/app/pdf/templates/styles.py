"""Shared `ParagraphStyle` definitions for every PDF section builder.

Centralized so heading levels stay consistent (and so `ReportDocTemplate`
can recognize "H1"/"H2" style names to drive the table of contents and PDF
outline — see `page_template.py`).
"""

from __future__ import annotations

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1

from app.pdf import theme


def build_stylesheet() -> StyleSheet1:
    styles = StyleSheet1()

    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName=theme.FONT_BOLD,
            fontSize=28,
            leading=34,
            textColor=theme.WHITE,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            fontName=theme.FONT_REGULAR,
            fontSize=13,
            leading=18,
            textColor=theme.SLATE_100,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMetaLabel",
            fontName=theme.FONT_BOLD,
            fontSize=9,
            leading=12,
            textColor=theme.SLATE_300,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMetaValue",
            fontName=theme.FONT_REGULAR,
            fontSize=11.5,
            leading=15,
            textColor=theme.WHITE,
        )
    )

    # H1/H2 style *names* are load-bearing: ReportDocTemplate.afterFlowable
    # matches on them to build the table of contents and outline bookmarks.
    styles.add(
        ParagraphStyle(
            name="H1",
            fontName=theme.FONT_BOLD,
            fontSize=18,
            leading=22,
            textColor=theme.PRIMARY_DARK,
            spaceBefore=4,
            spaceAfter=12,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            fontName=theme.FONT_BOLD,
            fontSize=13,
            leading=17,
            textColor=theme.SLATE_900,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOCTitle",
            fontName=theme.FONT_BOLD,
            fontSize=18,
            leading=22,
            textColor=theme.PRIMARY_DARK,
            spaceBefore=4,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            fontName=theme.FONT_REGULAR,
            fontSize=10,
            leading=15,
            textColor=theme.SLATE_700,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyMuted",
            fontName=theme.FONT_OBLIQUE,
            fontSize=9.5,
            leading=14,
            textColor=theme.SLATE_500,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Bullet",
            fontName=theme.FONT_REGULAR,
            fontSize=10,
            leading=14,
            textColor=theme.SLATE_700,
            leftIndent=14,
            bulletIndent=2,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeader",
            fontName=theme.FONT_BOLD,
            fontSize=9,
            leading=12,
            textColor=theme.WHITE,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName=theme.FONT_REGULAR,
            fontSize=9,
            leading=13,
            textColor=theme.SLATE_700,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardTitle",
            fontName=theme.FONT_BOLD,
            fontSize=11.5,
            leading=15,
            textColor=theme.SLATE_900,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardBody",
            fontName=theme.FONT_REGULAR,
            fontSize=9.5,
            leading=14,
            textColor=theme.SLATE_700,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardMeta",
            fontName=theme.FONT_BOLD,
            fontSize=8.5,
            leading=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOCEntry",
            fontName=theme.FONT_REGULAR,
            fontSize=11,
            leading=18,
            textColor=theme.SLATE_700,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOCEntry2",
            fontName=theme.FONT_REGULAR,
            fontSize=10,
            leading=16,
            leftIndent=14,
            textColor=theme.SLATE_500,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterText",
            fontName=theme.FONT_REGULAR,
            fontSize=7.5,
            leading=10,
            textColor=theme.SLATE_500,
            alignment=TA_CENTER,
        )
    )
    return styles
