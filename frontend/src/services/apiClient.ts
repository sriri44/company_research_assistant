// The only module that knows how to make an HTTP request. Every
// `*Service.ts` file calls through here — components never call `fetch`
// directly. See docs/ARCHITECTURE.md (frontend `services/`).
//
// Endpoint-specific logic is intentionally NOT implemented in Phase 1 (see
// docs/ROADMAP.md Phase 2) — this only defines the request/response
// contract shape via `ApiResult<T>`.

import { config } from "@/config/env";
import type { ApiResult } from "@/types/api";

export async function apiRequest<T>(
  path: string,
  init?: RequestInit,
): Promise<ApiResult<T>> {
  const response = await fetch(`${config.apiBaseUrl}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  return (await response.json()) as ApiResult<T>;
}
