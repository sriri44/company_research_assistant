"""FastAPI dependency provider for `CompanyService`."""

from __future__ import annotations

from app.core.container import get_container
from app.services.interfaces.company_service import CompanyService


def get_company_service() -> CompanyService:
    return get_container().company_service
