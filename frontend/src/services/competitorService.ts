// Typed client for /api/v1/competitors (see docs/API_DESIGN.md). Endpoint
// wiring lands in Phase 4 — method bodies are placeholders until then.

import type { Competitor } from "@/types/competitor";

export const competitorService = {
  async getForCompany(_companyId: string): Promise<Competitor[]> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 4");
  },
};
