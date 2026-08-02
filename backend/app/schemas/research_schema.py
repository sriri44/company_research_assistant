"""Research resource schemas — the HTTP contract for `POST
/api/v1/research`. Field names intentionally match the requested response
shape (`company_name`, `growth_opportunities`, ...) for this endpoint
rather than the rest of the app's camelCase-at-the-frontend convention,
since this exact shape is the literal contract for this resource.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=200, description="Company name or website URL")
    model: str | None = Field(
        default=None, description="OpenRouter model id; falls back to the server default if omitted"
    )


class CompetitorSchema(BaseModel):
    name: str
    website: str | None = None
    reason: str | None = None
    market_position: str | None = None


class GrowthOpportunitySchema(BaseModel):
    title: str
    description: str
    business_impact: str
    implementation_complexity: str
    priority_score: float
    estimated_roi: str | None = None


class ResearchResultSchema(BaseModel):
    report_id: str
    status: str
    company_name: str
    website: str
    phone: str | None = None
    address: str | None = None
    summary: str | None = None
    industry: str | None = None
    products: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    competitors: list[CompetitorSchema] = Field(default_factory=list)
    growth_opportunities: list[GrowthOpportunitySchema] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    confidence: float | None = None
