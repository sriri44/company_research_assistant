"""FastAPI dependency provider for `DiscordService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.discord_service import DiscordService


def get_discord_service() -> DiscordService:
    return get_container().discord_service
