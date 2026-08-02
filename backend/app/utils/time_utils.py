"""Time helpers.

Centralizes "what time is it" so every timestamp in the app (log lines,
response envelopes, domain models) uses the same timezone-aware source.
"""

from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current time as a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)
