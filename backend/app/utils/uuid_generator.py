"""UUID generation helper."""

from __future__ import annotations

from uuid import uuid4


def generate_uuid() -> str:
    """Return a new random UUID4 as a string."""
    return str(uuid4())
