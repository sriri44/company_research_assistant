"""Shared API envelope schemas.

Every endpoint response — success or error — is shaped by one of these, so
the frontend has exactly one parsing path (docs/ARCHITECTURE.md §10-11).
Route handlers return `SuccessResponse[T]` (built via
`app.utils.response_helper.build_success_response`);
`app.middleware.error_handler` is the only place `ErrorResponse` is built
(via `app.utils.error_helper.build_error_response`).
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.utils.time_utils import utcnow
from app.utils.uuid_generator import generate_uuid

T = TypeVar("T")


class ResponseMeta(BaseModel):
    request_id: str = Field(default_factory=generate_uuid)
    timestamp: str = Field(default_factory=lambda: utcnow().isoformat())


class PaginationMeta(ResponseMeta):
    page: int
    page_size: int
    total: int


class BaseResponse(BaseModel):
    """Common fields shared by every response envelope."""

    success: bool
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class SuccessResponse(BaseResponse, Generic[T]):
    success: bool = True
    data: T


class ApiError(BaseModel):
    code: str
    message: str
    details: list[str] = Field(default_factory=list)


class ErrorResponse(BaseResponse):
    success: bool = False
    error: ApiError
