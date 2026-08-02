"""PDF generation boundary.

Wraps ReportLab. `templates/` defines overall page layout; `builders/`
holds composable section builders (cover, summary, competitors,
opportunities). Consumed only by `ReportService`'s implementation —
receives already-generated report data, never fetches anything itself.
"""
