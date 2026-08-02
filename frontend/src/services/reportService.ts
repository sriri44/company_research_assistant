// Typed client for /api/v1/reports (see docs/API_DESIGN.md).
// `generate`/`getById` wiring is still Phase 6 future work — placeholders
// until report generation becomes an async job. `downloadPdf` is real: it
// hits the one wired-up report endpoint, GET /api/v1/report/{id}/pdf.

import axios from "axios";

import { api, ApiError } from "@/services/api";
import type { ApiErrorResponse } from "@/types/api";
import type { Report } from "@/types/report";

const FILENAME_FALLBACK = "research-report.pdf";

function filenameFromContentDisposition(headerValue: unknown): string {
  if (typeof headerValue !== "string") return FILENAME_FALLBACK;
  const match = /filename="?([^"]+)"?/.exec(headerValue);
  return match?.[1] ?? FILENAME_FALLBACK;
}

/** Blob error responses never get axios's usual `error.response.data`
 * JSON parsing (the whole point of `responseType: "blob"` is to leave the
 * body untouched), so a failed PDF request has to be re-decoded by hand to
 * surface the real backend error message instead of a generic one. */
async function toPdfApiError(error: unknown): Promise<ApiError> {
  if (axios.isAxiosError(error) && error.response?.data instanceof Blob) {
    try {
      const text = await error.response.data.text();
      const body = JSON.parse(text) as ApiErrorResponse;
      if (body?.error) {
        return new ApiError(body.error.message, body.error.code, body.error.details, error.response.status);
      }
    } catch {
      // Fall through to the generic error below — the blob wasn't JSON.
    }
  }
  if (axios.isAxiosError(error) && !error.response) {
    return new ApiError("Could not reach the server. Check that the backend is running and try again.", "NETWORK_ERROR");
  }
  return new ApiError("Something went wrong while generating the PDF. Please try again.", "UNKNOWN_ERROR");
}

export const reportService = {
  async generate(_companyId: string): Promise<Report> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 6");
  },
  async getById(_reportId: string): Promise<Report> {
    throw new Error("Not implemented — see docs/ROADMAP.md Phase 6");
  },

  /** Downloads the PDF for `reportId` and triggers the browser's native
   * save/download flow — no separate "save as" step needed. */
  async downloadPdf(reportId: string): Promise<void> {
    let response;
    try {
      response = await api.get(`/api/v1/report/${encodeURIComponent(reportId)}/pdf`, {
        responseType: "blob",
      });
    } catch (error) {
      throw await toPdfApiError(error);
    }

    const blob = new Blob([response.data], { type: "application/pdf" });
    const filename = filenameFromContentDisposition(response.headers["content-disposition"]);
    const objectUrl = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = objectUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(objectUrl);
  },
};
