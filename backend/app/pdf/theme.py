"""Visual language for generated PDF reports: colors, fonts, spacing.

Kept separate from `templates/` and `builders/` so the "what does this
report look like" decisions live in exactly one place. Uses ReportLab's
built-in Helvetica family only — no font files to bundle/ship, so
rendering is identical on every machine (dev laptop, Render container)
with zero deployment risk.
"""

from __future__ import annotations

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

PAGE_SIZE = A4
PAGE_WIDTH, PAGE_HEIGHT = A4

MARGIN_LEFT = 2.0 * cm
MARGIN_RIGHT = 2.0 * cm
MARGIN_TOP = 2.6 * cm
MARGIN_BOTTOM = 2.2 * cm

# Distance from the margin edge to the header/footer rule lines, and the
# cover page's own (wider, full-bleed) padding.
HEADER_RULE_OFFSET = 0.9 * cm
FOOTER_RULE_OFFSET = 0.5 * cm
COVER_PADDING = 2.5 * cm
COVER_PADDING_TOP = 3.2 * cm

# Brand palette — indigo/violet primary to match the product's own UI,
# slate neutrals for body text, semantic colors for impact/complexity/
# severity badges.
PRIMARY = HexColor("#4F46E5")
PRIMARY_DARK = HexColor("#312E81")
ACCENT = HexColor("#7C3AED")

SLATE_900 = HexColor("#0F172A")
SLATE_700 = HexColor("#334155")
SLATE_500 = HexColor("#64748B")
SLATE_300 = HexColor("#CBD5E1")
SLATE_100 = HexColor("#F1F5F9")
SLATE_50 = HexColor("#F8FAFC")
WHITE = HexColor("#FFFFFF")

SUCCESS = HexColor("#15803D")
SUCCESS_BG = HexColor("#DCFCE7")
WARNING = HexColor("#B45309")
WARNING_BG = HexColor("#FEF3C7")
DANGER = HexColor("#B91C1C")
DANGER_BG = HexColor("#FEE2E2")

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_OBLIQUE = "Helvetica-Oblique"

SEVERITY_COLORS = {
    "high": (DANGER, DANGER_BG),
    "medium": (WARNING, WARNING_BG),
    "low": (SUCCESS, SUCCESS_BG),
}
