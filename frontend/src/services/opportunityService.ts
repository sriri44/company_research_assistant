// Typed client for /api/v1/opportunities — AI Growth Opportunities(tm)
// (see docs/API_DESIGN.md). Endpoint wiring lands in Phase 5 — method
// bodies are placeholders until then.

import type { Opportunity } from "@/types/opportunity";

export const opportunityService = {
  async getForCompany(_companyId: string): Promise<Opportunity[]> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 5");
  },
};
