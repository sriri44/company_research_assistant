"""Helper for building the standard success response envelope
(`app.schemas.common.SuccessResponse`), used by route handlers so they
never construct the envelope by hand.
"""

from __future__ import annotations

from typing import TypeVar

from app.schemas.common import SuccessResponse

T = TypeVar("T")


def build_success_response(data: T) -> SuccessResponse[T]:
    """Wrap `data` in the standard success envelope."""
    return SuccessResponse(data=data)
