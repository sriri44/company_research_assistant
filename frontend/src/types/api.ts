// Mirrors backend/app/schemas/common.py — the standard response/error
// envelope every endpoint returns. See docs/ARCHITECTURE.md §10-11.
//
// Field names are snake_case to match the actual JSON on the wire —
// Pydantic does not camelCase by default and no alias generator is
// configured backend-side (verified against a live response).

export interface ResponseMeta {
  request_id: string;
  timestamp: string;
}

export interface PaginationMeta extends ResponseMeta {
  page: number;
  page_size: number;
  total: number;
}

export interface ApiResponse<T> {
  success: true;
  data: T;
  meta: ResponseMeta;
}

export interface ApiErrorDetail {
  code: string;
  message: string;
  details: string[];
}

export interface ApiErrorResponse {
  success: false;
  error: ApiErrorDetail;
  meta: ResponseMeta;
}

export type ApiResult<T> = ApiResponse<T> | ApiErrorResponse;
