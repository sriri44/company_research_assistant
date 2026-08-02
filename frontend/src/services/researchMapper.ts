// Translates the raw backend response (types/researchApi.ts, snake_case,
// exact wire format) into the UI-facing ResearchResult shape the Phase 3
// components (CompanyCard, CompetitorCard, OpportunityCard,
// ResearchSummary) were already built against — isolating every bit of
// "what the backend actually calls this field" knowledge in one place.

import type { Competitor } from "@/types/competitor";
import type { Opportunity } from "@/types/opportunity";
import type { CompanyProfile, ResearchResult } from "@/types/research";
import type { CompetitorApiItem, GrowthOpportunityApiItem, ResearchApiResult } from "@/types/researchApi";

function stripToDomain(website: string | null): string {
  if (!website) return "";
  const withScheme = website.startsWith("http://") || website.startsWith("https://") ? website : `https://${website}`;
  try {
    return new URL(withScheme).hostname.replace(/^www\./, "");
  } catch {
    return website;
  }
}

function toCompetitor(item: CompetitorApiItem, rank: number): Competitor {
  return {
    name: item.name,
    domain: stripToDomain(item.website) || item.name.toLowerCase().replace(/\s+/g, ""),
    // The backend doesn't return a numeric similarity score — same
    // rank-based heuristic as the backend's own AI-result mapper
    // (app/ai/mappers.py) for a consistent "most-relevant-first" feel.
    similarityScore: Math.max(0.3, Math.round((1 - rank * 0.15) * 100) / 100),
    summary: item.reason,
    marketPosition: item.market_position,
  };
}

function toOpportunity(item: GrowthOpportunityApiItem): Opportunity {
  return {
    title: item.title,
    description: item.description,
    category: "AI Growth Opportunity",
    impact: item.business_impact,
    complexity: item.implementation_complexity,
    priorityScore: item.priority_score,
    estimatedRoi: item.estimated_roi,
  };
}

export function mapResearchResponse(data: ResearchApiResult): ResearchResult {
  const company: CompanyProfile = {
    id: data.report_id,
    name: data.company_name,
    domain: data.website,
    aliases: [],
    industry: data.industry,
    description: data.summary,
    resolvedAt: new Date().toISOString(),
    phone: data.phone,
    address: data.address,
    summary: data.summary ?? "No summary available.",
    painPoints: data.pain_points,
  };

  return {
    company,
    competitors: data.competitors.map(toCompetitor),
    opportunities: [...data.growth_opportunities]
      .sort((a, b) => b.priority_score - a.priority_score)
      .map(toOpportunity),
    sources: data.sources,
    confidence: data.confidence,
  };
}
