"""Search boundary.

Wraps Serper.dev so the rest of the application never imports it directly.
`SearchService` (see `app.services.interfaces.search_service`) is the only
public contract other layers depend on.
"""
