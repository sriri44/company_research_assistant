"""Placeholder CompanyService.

Satisfies the `CompanyService` interface so the DI graph and API layer are
wireable before a real implementation exists. Every method raises
`NotImplementedError` — no business logic. See docs/ROADMAP.md Phase 2.
"""

from __future__ import annotations

from app.models.company import Company
from app.services.interfaces.company_service import CompanyService


class PlaceholderCompanyService(CompanyService):
    async def resolve(self, raw_input: str) -> Company:
        raise NotImplementedError(
            "CompanyService.resolve is not implemented yet — see docs/ROADMAP.md"
        )

    async def get_by_id(self, company_id: str) -> Company:
        raise NotImplementedError(
            "CompanyService.get_by_id is not implemented yet — see docs/ROADMAP.md"
        )
