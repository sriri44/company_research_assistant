"""Logger helper — the standard way any module obtains a logger.

Handler/formatter/rotation setup happens once, at startup, in
`app.core.logging.configure_logging`. This function just wraps
`logging.getLogger` so call sites have one stable, discoverable import
instead of reaching into the stdlib module directly.
"""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a logger for `name` (conventionally `__name__`)."""
    return logging.getLogger(name)
