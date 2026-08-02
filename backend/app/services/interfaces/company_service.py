"""CompanyService interface.

Responsibility: resolve raw user input (a company name or a website URL)
into a canonical `Company` domain identity that every downstream service
(search, crawler, AI, competitor, opportunity) can rely on.

Out of scope: searching the web, crawling, or AI analysis — this service
only establishes *who* the company is, not what it does.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.company import Company


class CompanyService(ABC):
    @abstractmethod
    async def resolve(self, raw_input: str) -> Company:
        """Resolve a company name or URL into a canonical `Company`.

        Raises a domain-specific exception (see `app.core.exceptions`) if
        the input cannot be resolved to a company identity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, company_id: str) -> Company:
        """Fetch a previously resolved company by its internal id."""
        raise NotImplementedError
