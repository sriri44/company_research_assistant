"""Helper for building the standard error response envelope
(`app.schemas.common.ErrorResponse`), used exclusively by
`app.middleware.error_handler` so every failure path produces the same
shape.
"""

from __future__ import annotations

from app.schemas.common import ApiError, ErrorResponse


def build_error_response(
    code: str,
    message: str,
    details: list[str] | None = None,
) -> ErrorResponse:
    """Build a standard error envelope for an exception handler to return."""
    return ErrorResponse(error=ApiError(code=code, message=message, details=details or []))
