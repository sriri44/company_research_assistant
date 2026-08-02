// Research pipeline UI types — drives the progress Timeline and result
// display on the Research page. The step list is presentational (the real
// backend is a single synchronous call with no stage-by-stage streaming —
// see useConversationStore for how progress is paced client-side); the
// result shapes are populated from the real POST /api/v1/research response
// via researchMapper.ts.

import type { Company } from "./company";
import type { Competitor } from "./competitor";
import type { Opportunity } from "./opportunity";

export type ResearchStepId =
  | "resolve"
  | "search"
  | "crawl"
  | "analyze"
  | "competitors"
  | "opportunities"
  | "report";

export type ResearchStepStatus = "pending" | "active" | "complete";

export interface ResearchStep {
  id: ResearchStepId;
  label: string;
  description: string;
  status: ResearchStepStatus;
}

export type ResearchSessionStatus = "idle" | "running" | "complete" | "error";

/** Extends the backend-mirrored `Company` with the richer display fields
 * the research pipeline produces. `founded`/`headquarters`/`employeeCount`
 * are optional — the real backend doesn't return them (they were only
 * ever mock-data fields); `CompanyCard` renders only the ones present. */
export interface CompanyProfile extends Company {
  founded?: string | null;
  headquarters?: string | null;
  employeeCount?: string | null;
  phone?: string | null;
  address?: string | null;
  summary: string;
  painPoints: string[];
}

export interface ResearchResult {
  company: CompanyProfile;
  competitors: Competitor[];
  opportunities: Opportunity[];
  sources: string[];
  confidence: number | null;
}
