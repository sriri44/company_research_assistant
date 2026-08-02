"""Table of Contents section.

Returns the `TableOfContents` flowable itself — entries are populated
automatically as the document builds, via `ReportDocTemplate.afterFlowable`
noticing "H1"/"H2" headings (see `templates/page_template.py`). Requires
`doc.multiBuild()` so page numbers are correct on the rendered copy.
"""

from __future__ import annotations

from reportlab.lib.styles import StyleSheet1
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Spacer
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.tableofcontents import TableOfContents


def build_toc_section(styles: StyleSheet1) -> list[Flowable]:
    toc = TableOfContents()
    toc.levelStyles = [styles["TOCEntry"], styles["TOCEntry2"]]
    toc.dotsMinLevel = 0

    return [
        NextPageTemplate("Content"),
        PageBreak(),
        Paragraph("Table of Contents", styles["TOCTitle"]),
        Spacer(1, 6),
        toc,
        PageBreak(),
    ]
