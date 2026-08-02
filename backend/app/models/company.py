"""Domain model: Company.

Represents a resolved company identity — the canonical output of
`CompanyService` and the input every downstream service (search, crawler,
AI, competitor, opportunity) keys off of.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Company:
    id: str
    name: str
    domain: str
    aliases: list[str] = field(default_factory=list)
    industry: str | None = None
    description: str | None = None
    resolved_at: datetime | None = None
