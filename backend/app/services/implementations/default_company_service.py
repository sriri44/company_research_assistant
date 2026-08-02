"""Search-backed CompanyService implementation.

Resolves a raw name/URL into a canonical `Company`. A URL/domain input
skips search entirely (per spec: search is only needed to find an
*unknown* website); a plain name is resolved via
`SearchService.search_query`, filtering out non-official-site domains
(Wikipedia, social platforms, etc.). Resolved companies are cached
in-memory (id -> Company) for the process lifetime so `get_by_id` works
after `resolve` — there is no database in this phase.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from app.core.exceptions import CompanyNotFoundError
from app.models.company import Company
from app.services.interfaces.company_service import CompanyService
from app.services.interfaces.search_service import SearchService
from app.utils.logger import get_logger
from app.utils.time_utils import utcnow
from app.utils.uuid_generator import generate_uuid

logger = get_logger(__name__)

_URL_RE = re.compile(r"^(https?://)?([\w-]+\.)+[a-z]{2,}(/.*)?$", re.IGNORECASE)
_EXCLUDED_DOMAINS = (
    "wikipedia.org",
    "linkedin.com",
    "facebook.com",
    "twitter.com",
    "x.com",
    "instagram.com",
    "youtube.com",
    "crunchbase.com",
    "google.com",
    "bloomberg.com",
    "reddit.com",
)


class DefaultCompanyService(CompanyService):
    def __init__(self, search_service: SearchService) -> None:
        self._search_service = search_service
        self._cache: dict[str, Company] = {}

    async def resolve(self, raw_input: str) -> Company:
        cleaned = raw_input.strip()
        if not cleaned:
            raise CompanyNotFoundError("No company name or URL was provided.")

        domain = _extract_domain(cleaned)
        if domain is not None:
            logger.info("Company input %r recognized as a URL — skipping search.", cleaned)
        else:
            logger.info("Searching for official website of %r", cleaned)
            domain = await self._resolve_domain_via_search(cleaned)
            logger.info("Website resolved: %s -> %s", cleaned, domain)

        name = _guess_name(cleaned, domain)
        company = Company(
            id=generate_uuid(),
            name=name,
            domain=domain,
            aliases=[cleaned] if cleaned.lower() != name.lower() else [],
            resolved_at=utcnow(),
        )
        self._cache[company.id] = company
        return company

    async def get_by_id(self, company_id: str) -> Company:
        company = self._cache.get(company_id)
        if company is None:
            raise CompanyNotFoundError(f"No resolved company found for id={company_id}")
        return company

    async def _resolve_domain_via_search(self, name: str) -> str:
        results = await self._search_service.search_query(f"{name} official website", limit=5)
        for url in results:
            domain = _extract_domain(url)
            if domain and not _is_excluded(domain):
                return domain
        raise CompanyNotFoundError(f"Could not resolve an official website for {name!r}.")


def _extract_domain(candidate: str) -> str | None:
    text = candidate.strip()
    if not _URL_RE.match(text):
        return None
    if not text.startswith(("http://", "https://")):
        text = f"https://{text}"
    netloc = urlparse(text).netloc
    return netloc[4:] if netloc.startswith("www.") else netloc


def _is_excluded(domain: str) -> bool:
    return any(
        domain == excluded or domain.endswith(f".{excluded}") for excluded in _EXCLUDED_DOMAINS
    )


def _guess_name(raw_input: str, domain: str) -> str:
    """A placeholder display name used only until the AI analysis returns
    `company_name` — `ResearchReportService` overrides it with the AI's
    (more accurate) answer once available."""
    if _URL_RE.match(raw_input.strip()):
        label = domain.split(".")[0]
        return label.replace("-", " ").title()
    return raw_input.strip()
