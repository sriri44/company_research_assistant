"""System resource routes — mounted at `/api/v1/system`.

Reserved for versioned, API-consumer-facing system/admin endpoints (e.g.
detailed diagnostics), distinct from the unversioned infra probes in
`health_routes.py`. Stubbed with HTTP 501 until a real use case lands.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/status")
async def system_status() -> None:
    """Detailed system/diagnostics status for API consumers."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not Implemented")
