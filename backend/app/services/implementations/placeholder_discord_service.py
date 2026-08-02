"""Placeholder DiscordService.

Satisfies the `DiscordService` interface so the DI graph and API layer are
wireable before a real Discord-backed implementation exists. See
docs/ROADMAP.md Phase 7.
"""

from __future__ import annotations

from app.models.report import Report
from app.services.interfaces.discord_service import DiscordService


class PlaceholderDiscordService(DiscordService):
    async def deliver_report(self, report: Report, target: str = "default") -> bool:
        raise NotImplementedError(
            "DiscordService.deliver_report is not implemented yet — see docs/ROADMAP.md"
        )
