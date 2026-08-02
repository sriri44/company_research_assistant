"""DiscordService interface.

Responsibility: deliver a finished `Report` (or a summary of it) to a
configured Discord destination (webhook or bot).

Out of scope: report generation/composition — this service only handles
outbound delivery.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.report import Report


class DiscordService(ABC):
    @abstractmethod
    async def deliver_report(self, report: Report, target: str = "default") -> bool:
        """Send the report to the given Discord target. Returns True on
        confirmed delivery."""
        raise NotImplementedError
