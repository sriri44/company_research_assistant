// Typed client for /api/v1/companies (see docs/API_DESIGN.md). Endpoint
// wiring lands in Phase 2 — method bodies are placeholders until then.

import type { Company } from "@/types/company";

export const companyService = {
  async resolve(_input: string): Promise<Company> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 2");
  },
};
