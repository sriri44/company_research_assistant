// Typed client for /api/v1/reports (see docs/API_DESIGN.md). Endpoint
// wiring lands in Phase 6 — method bodies are placeholders until then.

import type { Report } from "@/types/report";

export const reportService = {
  async generate(_companyId: string): Promise<Report> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 6");
  },
  async getById(_reportId: string): Promise<Report> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 6");
  },
};
