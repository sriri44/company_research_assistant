// Typed client for POST/GET /api/v1/research — the one real backend
// integration this app has (see docs/ROADMAP.md Phase 4). All other
// service stubs (companyService.ts, reportService.ts, ...) still throw
// "Not implemented" since their backend routes are still 501 stubs.

import { request } from "@/services/api";
import type { ApiResponse } from "@/types/api";
import type { ResearchApiResult, ResearchRequestPayload } from "@/types/researchApi";

export interface StartResearchParams {
  query: string;
  model: string;
  signal?: AbortSignal;
}

export const researchService = {
  async startResearch({ query, model, signal }: StartResearchParams): Promise<ResearchApiResult> {
    const payload: ResearchRequestPayload = { query, model };
    const response = await request<ApiResponse<ResearchApiResult>>({
      method: "POST",
      url: "/api/v1/research",
      data: payload,
      signal,
    });
    return response.data;
  },

  async getResearch(reportId: string, signal?: AbortSignal): Promise<ResearchApiResult> {
    const response = await request<ApiResponse<ResearchApiResult>>({
      method: "GET",
      url: `/api/v1/research/${encodeURIComponent(reportId)}`,
      signal,
    });
    return response.data;
  },
};
