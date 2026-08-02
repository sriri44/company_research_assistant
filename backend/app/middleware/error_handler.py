"""Global exception handling.

`register_exception_handlers` is the single place that turns any failure —
request validation, an intentionally raised `HTTPException`, a domain
`AppError`, or anything unhandled — into the standard error envelope
(docs/ARCHITECTURE.md §11). No route or service should ever build an error
response by hand.
"""

from __future__ import annotations

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.utils.error_helper import build_error_response
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        f"{'.'.join(str(loc) for loc in error['loc'])}: {error['msg']}" for error in exc.errors()
    ]
    body = build_error_response(
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        details=details,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=body.model_dump()
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    body = build_error_response(
        code=_code_for_status(exc.status_code),
        message=str(exc.detail),
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    body = build_error_response(code=exc.code, message=exc.message, details=exc.details)
    return JSONResponse(status_code=exc.http_status, content=body.model_dump())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    body = build_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
    )
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=body.model_dump()
    )
    _attach_cors_headers(request, response)
    return response


def _attach_cors_headers(request: Request, response: JSONResponse) -> None:
    """Starlette routes handlers registered for the base `Exception` class
    through `ServerErrorMiddleware`, which wraps *outside* our
    `CORSMiddleware` — so, unlike every other error path in this file,
    this response never passes back through it and never gets CORS
    headers applied. Without this, an unexpected bug looks like a CORS
    failure in the browser instead of the real error. Only mirrors the
    request's Origin back if it's actually on the allow-list."""
    origin = request.headers.get("origin")
    if origin and origin in get_settings().cors_allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"


def _code_for_status(status_code: int) -> str:
    return {
        status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
        status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
        status.HTTP_403_FORBIDDEN: "FORBIDDEN",
        status.HTTP_404_NOT_FOUND: "NOT_FOUND",
        status.HTTP_422_UNPROCESSABLE_CONTENT: "VALIDATION_ERROR",
        status.HTTP_429_TOO_MANY_REQUESTS: "RATE_LIMITED",
        status.HTTP_501_NOT_IMPLEMENTED: "NOT_IMPLEMENTED",
    }.get(status_code, "HTTP_ERROR")


def register_exception_handlers(app: FastAPI) -> None:
    # Starlette's `add_exception_handler` stub is invariant on the handler's
    # exception parameter, so registering a handler narrower than `Exception`
    # is a known false positive under mypy --strict — the runtime behavior
    # (dispatch by exception type, most specific match wins) is correct.
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)
