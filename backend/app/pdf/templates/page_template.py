"""The document-level ReportLab template: page geometry, running header/
footer, page numbers, and table-of-contents/outline wiring.

`ReportDocTemplate` is a `BaseDocTemplate` with two `PageTemplate`s — a
full-bleed "Cover" page (drawn once, no header/footer) and a "Content"
page reused for every subsequent page (drawn via `onPage`, gets the
running header/footer). Section builders switch page templates by
inserting a `NextPageTemplate("Content")` flowable into the story.

Requires `doc.multiBuild(story)` (not `.build()`) — the table of contents
needs a first pass to learn each heading's final page number before it can
render correctly on the second pass.
"""

from __future__ import annotations

from typing import Any

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.paragraph import Paragraph

from app.pdf import theme

_HEADING_STYLES = {"H1": 0, "H2": 1}


class ReportDocTemplate(BaseDocTemplate):  # type: ignore[misc]
    # ReportLab ships no type stubs, so `BaseDocTemplate` resolves to `Any`
    # under `ignore_missing_imports` — mypy --strict flags subclassing
    # `Any` even though this is a completely ordinary subclass at runtime
    # (see the identical pattern/rationale in app/middleware/error_handler.py).
    def __init__(
        self,
        filename: Any,
        *,
        company_name: str,
        generated_label: str,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("pagesize", theme.PAGE_SIZE)
        kwargs.setdefault("topMargin", theme.MARGIN_TOP)
        kwargs.setdefault("bottomMargin", theme.MARGIN_BOTTOM)
        kwargs.setdefault("leftMargin", theme.MARGIN_LEFT)
        kwargs.setdefault("rightMargin", theme.MARGIN_RIGHT)
        kwargs.setdefault("title", f"{company_name} — AI Company Research Report")
        kwargs.setdefault("author", "AI Company Research Assistant")
        super().__init__(filename, **kwargs)

        self.company_name = company_name
        self.generated_label = generated_label
        self._bookmark_seq = 0

        cover_frame = Frame(
            0,
            0,
            theme.PAGE_WIDTH,
            theme.PAGE_HEIGHT,
            leftPadding=theme.COVER_PADDING,
            rightPadding=theme.COVER_PADDING,
            topPadding=theme.COVER_PADDING_TOP,
            bottomPadding=theme.COVER_PADDING,
            id="cover",
        )
        content_frame = Frame(
            theme.MARGIN_LEFT,
            theme.MARGIN_BOTTOM,
            theme.PAGE_WIDTH - theme.MARGIN_LEFT - theme.MARGIN_RIGHT,
            theme.PAGE_HEIGHT - theme.MARGIN_TOP - theme.MARGIN_BOTTOM,
            id="content",
        )

        self.addPageTemplates(
            [
                PageTemplate(id="Cover", frames=[cover_frame], onPage=self._draw_cover_page),
                PageTemplate(id="Content", frames=[content_frame], onPage=self._draw_content_page),
            ]
        )

    def build(self, flowables: list[Flowable], **kwargs: Any) -> None:
        # `multiBuild` re-runs `build()` from scratch on every pass without
        # reconstructing this doc, so counters seeded in __init__ must be
        # reset here too — otherwise bookmark keys keep incrementing across
        # passes, the TOC's entry tuples (which include the key) never
        # compare equal to the previous pass, and multiBuild never
        # converges (raises IndexError after maxPasses).
        self._bookmark_seq = 0
        super().build(flowables, **kwargs)

    # -- table of contents + PDF outline -------------------------------
    def afterFlowable(self, flowable: object) -> None:
        if not isinstance(flowable, Paragraph):
            return
        style_name = getattr(flowable.style, "name", "")
        level = _HEADING_STYLES.get(style_name)
        if level is None:
            return

        text = flowable.getPlainText()
        self._bookmark_seq += 1
        key = f"toc-{self._bookmark_seq}"
        self.canv.bookmarkPage(key)
        # The PDF outline (sidebar bookmarks) is a document-metadata string,
        # not page content — ReportLab doesn't run it through the same
        # WinAnsi text-rendering path as an in-page Paragraph, so characters
        # like "™" that render fine on the page can come out mangled in a
        # viewer's bookmark panel. ASCII-fold just the outline title; the
        # in-page TOC keeps the real glyph via `notify` below.
        outline_title = text.replace("™", "(TM)").encode("ascii", "replace").decode("ascii")
        self.canv.addOutlineEntry(outline_title, key, level=level, closed=False)
        self.notify("TOCEntry", (level, text, self.page, key))

    # -- page drawing ----------------------------------------------------
    def _draw_cover_page(self, canvas: Canvas, doc: ReportDocTemplate) -> None:
        canvas.saveState()
        canvas.setFillColor(theme.PRIMARY_DARK)
        canvas.rect(0, 0, theme.PAGE_WIDTH, theme.PAGE_HEIGHT, fill=1, stroke=0)
        canvas.restoreState()

    def _draw_content_page(self, canvas: Canvas, doc: ReportDocTemplate) -> None:
        canvas.saveState()

        # Header
        canvas.setStrokeColor(theme.SLATE_300)
        canvas.setLineWidth(0.75)
        header_y = theme.PAGE_HEIGHT - theme.MARGIN_TOP + theme.HEADER_RULE_OFFSET
        canvas.line(theme.MARGIN_LEFT, header_y, theme.PAGE_WIDTH - theme.MARGIN_RIGHT, header_y)

        canvas.setFont(theme.FONT_BOLD, 9)
        canvas.setFillColor(theme.PRIMARY_DARK)
        canvas.drawString(theme.MARGIN_LEFT, header_y + 6, "AI Company Research Report")

        canvas.setFont(theme.FONT_REGULAR, 9)
        canvas.setFillColor(theme.SLATE_500)
        canvas.drawRightString(
            theme.PAGE_WIDTH - theme.MARGIN_RIGHT, header_y + 6, doc.company_name
        )

        # Footer
        footer_top = theme.MARGIN_BOTTOM - theme.FOOTER_RULE_OFFSET
        canvas.setStrokeColor(theme.SLATE_300)
        canvas.setLineWidth(0.75)
        canvas.line(
            theme.MARGIN_LEFT, footer_top, theme.PAGE_WIDTH - theme.MARGIN_RIGHT, footer_top
        )

        canvas.setFont(theme.FONT_REGULAR, 7.5)
        canvas.setFillColor(theme.SLATE_500)
        canvas.drawString(
            theme.MARGIN_LEFT,
            footer_top - 12,
            f"Generated by AI Company Research Assistant — {doc.generated_label}",
        )
        canvas.drawRightString(
            theme.PAGE_WIDTH - theme.MARGIN_RIGHT, footer_top - 12, f"Page {canvas.getPageNumber()}"
        )

        canvas.restoreState()
