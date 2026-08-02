"""Pydantic schemas for the single structured AI research response.

Distinct from `app.schemas` (HTTP-facing) and `app.models` (domain
objects) — this is purely the shape `OpenRouterAIService` validates the
model's JSON output against before `ResearchReportService` translates it
into domain objects (`Company`, `Competitor`, `Opportunity`, `Report`).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AICompetitor(BaseModel):
    name: str
    website: str | None = None
    reason: str
    market_position: str


class AIOpportunity(BaseModel):
    title: str
    description: str
    business_impact: Literal["low", "medium", "high"]
    implementation_complexity: Literal["low", "medium", "high"]
    priority_score: float = Field(ge=0, le=100)
    estimated_roi: str


class ResearchAnalysisResult(BaseModel):
    """The one structured object the AI returns per research run —
    company summary, competitors, and AI Growth Opportunities™ together,
    produced by a single model call (see docs on the "one AI call" rule
    in `research_report_service.py`)."""

    company_name: str
    website: str | None = None
    phone: str | None = None
    address: str | None = None
    summary: str
    industry: str | None = None
    products: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    competitors: list[AICompetitor] = Field(default_factory=list)
    growth_opportunities: list[AIOpportunity] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
