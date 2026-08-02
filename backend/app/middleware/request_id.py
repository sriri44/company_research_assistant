"""Request ID middleware.

Assigns a unique id to every request (reusing an inbound `X-Request-ID`
header if present) and publishes it via `request_id_var` so every log line
emitted while handling the request is correlated. Echoed back in the
`X-Request-ID` response header and in every response envelope's
`meta.request_id`.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import request_id_var
from app.utils.uuid_generator import generate_uuid

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or generate_uuid()
        token = request_id_var.set(request_id)
        request.state.request_id = request_id
        try:
            response = await call_next(request)
        finally:
            request_id_var.reset(token)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
