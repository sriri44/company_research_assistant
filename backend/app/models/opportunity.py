"""Domain model: Opportunity (AI Growth Opportunities(tm)).

Represents a single automation/growth opportunity identified for a company,
as produced by the `app.ai.opportunities` engine and exposed via
`OpportunityService`. This is the flagship feature's core data shape —
kept in its own module so scoring logic (impact/complexity/priority) has a
stable target to populate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ImpactLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComplexityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Opportunity:
    title: str
    description: str
    category: str
    impact: ImpactLevel
    complexity: ComplexityLevel
    priority_score: float
    estimated_roi: str | None = None
