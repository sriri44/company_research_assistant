"""Error logging middleware.

Logs unhandled exceptions (with the correlating request id already in
context, see `request_id.py`) before re-raising, so `error_handler.py`'s
exception handlers can still turn them into the standard JSON error
envelope. This middleware only logs — it never builds a response itself.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception:
            logger.exception(
                "Unhandled exception while processing %s %s", request.method, request.url.path
            )
            raise
