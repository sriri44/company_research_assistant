"""Config helper — a stable, discoverable import point for application
settings, re-exporting `app.core.config.get_settings` alongside the other
utility helpers.
"""

from __future__ import annotations

from app.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Return the cached application `Settings` instance."""
    return get_settings()
