// Mirrors backend/app/schemas/research_schema.py exactly — the literal
// wire format of POST /api/v1/research, verified against a live response.
// Deliberately kept snake_case and separate from the UI-facing types in
// research.ts/competitor.ts/opportunity.ts: this file is the honest
// contract, researchMapper.ts translates it into what the existing
// (Phase 3) components already expect.

export interface ResearchRequestPayload {
  query: string;
  model: string;
}

export type ResearchApiStatus = "queued" | "processing" | "complete" | "failed";

export interface CompetitorApiItem {
  name: string;
  website: string | null;
  reason: string | null;
  market_position: string | null;
}

export interface GrowthOpportunityApiItem {
  title: string;
  description: string;
  business_impact: "low" | "medium" | "high";
  implementation_complexity: "low" | "medium" | "high";
  priority_score: number;
  estimated_roi: string | null;
}

export interface ResearchApiResult {
  report_id: string;
  status: ResearchApiStatus;
  company_name: string;
  website: string;
  phone: string | null;
  address: string | null;
  summary: string | null;
  industry: string | null;
  products: string[];
  services: string[];
  pain_points: string[];
  competitors: CompetitorApiItem[];
  growth_opportunities: GrowthOpportunityApiItem[];
  sources: string[];
  confidence: number | null;
}
