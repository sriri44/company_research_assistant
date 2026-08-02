// The reusable axios client every service calls through — central error
// normalization, timeout, and single-retry-on-transient-failure live here
// exactly once. Components/stores never call axios directly.

import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosError } from "axios";

import type { ApiErrorResponse } from "@/types/api";
import { config } from "@/config/env";

const REQUEST_TIMEOUT_MS = 60_000; // research requests can legitimately take 20-30s+ (crawl + AI)
const RETRYABLE_STATUS_CODES = new Set([502, 503, 504]);

export class ApiError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly details: string[] = [],
    public readonly status?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export const api: AxiosInstance = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: REQUEST_TIMEOUT_MS,
  headers: { "Content-Type": "application/json" },
});

function isTransientFailure(error: AxiosError): boolean {
  if (error.code === "ECONNABORTED" || error.code === "ERR_NETWORK") return true;
  const status = error.response?.status;
  return status !== undefined && RETRYABLE_STATUS_CODES.has(status);
}

function toApiError(error: unknown): ApiError {
  if (axios.isCancel(error)) {
    return new ApiError("Request was cancelled.", "REQUEST_CANCELLED");
  }

  if (axios.isAxiosError(error)) {
    if (error.code === "ECONNABORTED") {
      return new ApiError(
        "The request took too long to respond. Please try again.",
        "TIMEOUT",
      );
    }
    if (!error.response) {
      return new ApiError(
        "Could not reach the server. Check that the backend is running and try again.",
        "NETWORK_ERROR",
      );
    }

    const body = error.response.data as ApiErrorResponse | undefined;
    if (body?.error) {
      return new ApiError(body.error.message, body.error.code, body.error.details, error.response.status);
    }
    return new ApiError(
      "Something went wrong. Please try again.",
      "UNKNOWN_ERROR",
      [],
      error.response.status,
    );
  }

  return new ApiError("An unexpected error occurred.", "UNKNOWN_ERROR");
}

/** Executes a request, retrying once for transient network/5xx failures
 * (never for 4xx — those won't succeed on retry, and never for a
 * cancelled request). Every failure — after any retry — is normalized
 * into an `ApiError` with a safe, user-facing message; no stack traces or
 * raw axios errors ever escape this function. */
export async function request<T>(requestConfig: AxiosRequestConfig): Promise<T> {
  try {
    const response = await api.request<T>(requestConfig);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && !axios.isCancel(error) && isTransientFailure(error)) {
      try {
        const response = await api.request<T>(requestConfig);
        return response.data;
      } catch (retryError) {
        throw toApiError(retryError);
      }
    }
    throw toApiError(error);
  }
}
