"""AI research pipeline orchestrator — the real ReportService implementation.

`run_research(query, model)` is the primary entry point (used by
`POST /api/v1/research`): resolve the company, crawl its site, build one
AI prompt from everything gathered, make exactly ONE AI call, and map the
single structured response into a `Report`. The locked `ReportService`
interface methods (`generate_report`, `get_report`) are implemented too,
for interface completeness, delegating to the same pipeline.

Pipeline: resolve -> crawl -> extract/clean -> ONE AI call -> map -> return.
Every stage is logged. Crawl and competitor-search failures degrade
gracefully (the AI call still runs on whatever was gathered); only a
total AI failure marks the report FAILED — there's nothing left to
analyze without it.
"""

from __future__ import annotations

import dataclasses

from app.ai.mappers import to_competitor, to_opportunity
from app.ai.schemas import ResearchAnalysisResult
from app.core.exceptions import (
    AIProviderError,
    CrawlerError,
    ReportNotFoundError,
    SearchProviderError,
)
from app.crawler.strategies.path_discovery import build_seed_urls, normalize_root_url
from app.crawler.types import CrawledPage
from app.models.company import Company
from app.models.report import Report, ReportStatus
from app.services.interfaces.ai_service import AIService
from app.services.interfaces.company_service import CompanyService
from app.services.interfaces.crawler_service import CrawlerService
from app.services.interfaces.report_service import ReportService
from app.services.interfaces.search_service import SearchService
from app.utils.logger import get_logger
from app.utils.text_cleaning import build_research_context
from app.utils.time_utils import utcnow
from app.utils.uuid_generator import generate_uuid

logger = get_logger(__name__)

_MAX_COMPETITOR_HINTS = 8


class ResearchReportService(ReportService):
    def __init__(
        self,
        company_service: CompanyService,
        search_service: SearchService,
        crawler_service: CrawlerService,
        ai_service: AIService,
        *,
        max_context_words: int,
    ) -> None:
        self._company_service = company_service
        self._search_service = search_service
        self._crawler_service = crawler_service
        self._ai_service = ai_service
        self._max_context_words = max_context_words
        self._reports: dict[str, Report] = {}

    async def run_research(self, query: str, model: str | None = None) -> Report:
        """The real pipeline entry point used by `POST /api/v1/research`."""
        logger.info("Searching company: %r", query)
        company = await self._company_service.resolve(query)

        report_id = generate_uuid()
        self._reports[report_id] = Report(
            id=report_id, company=company, status=ReportStatus.PROCESSING, created_at=utcnow()
        )

        pages = await self._crawl_company_site(company.domain)
        context = build_research_context(pages, max_words=self._max_context_words)
        competitor_hints = await self._gather_competitor_hints(company)

        try:
            logger.info("AI started for %s", company.domain)
            analysis = await self._analyze(company, context, competitor_hints, model)
        except AIProviderError as exc:
            logger.warning("AI analysis failed for %s: %s", company.domain, exc)
            report = dataclasses.replace(
                self._reports[report_id],
                status=ReportStatus.FAILED,
                summary=f"Research could not be completed: {exc}",
                sources=[page.url for page in pages],
                completed_at=utcnow(),
            )
            self._reports[report_id] = report
            logger.info(
                "Research completed for %s (status=%s)", company.domain, report.status.value
            )
            return report

        logger.info(
            "Competitors generated: %d, opportunities: %d, confidence=%.2f",
            len(analysis.competitors),
            len(analysis.growth_opportunities),
            analysis.confidence,
        )

        report = _build_report(
            report_id, company, analysis, sources=[page.url for page in pages] or analysis.sources
        )
        self._reports[report_id] = report
        logger.info("Research completed for %s (status=%s)", company.domain, report.status.value)
        return report

    async def generate_report(self, company_id: str) -> Report:
        company = await self._company_service.get_by_id(company_id)
        return await self.run_research(company.domain)

    async def get_report(self, report_id: str) -> Report:
        report = self._reports.get(report_id)
        if report is None:
            raise ReportNotFoundError(f"No report found for id={report_id}")
        return report

    async def _crawl_company_site(self, domain: str) -> list[CrawledPage]:
        root_url = normalize_root_url(domain)
        seed_urls = build_seed_urls(root_url)
        logger.info("Crawling started: %s (%d seed page(s))", root_url, len(seed_urls))

        try:
            pages = await self._crawler_service.crawl_many(seed_urls)
        except CrawlerError as exc:
            logger.warning(
                "Crawling failed entirely for %s, continuing with no content: %s", root_url, exc
            )
            return []

        logger.info("Pages crawled: %d", len(pages))
        return pages

    async def _gather_competitor_hints(self, company: Company) -> str:
        try:
            urls = await self._search_service.search_company(company, limit=_MAX_COMPETITOR_HINTS)
        except SearchProviderError as exc:
            logger.warning("Competitor search failed, continuing without hints: %s", exc)
            return "(competitor search unavailable)"
        return "\n".join(f"- {url}" for url in urls) or "(no candidate competitors found)"

    async def _analyze(
        self, company: Company, context: str, competitor_hints: str, model: str | None
    ) -> ResearchAnalysisResult:
        request_context: dict[str, object] = {
            "company_name": company.name,
            "website": company.domain,
            "context": context or "(no website content could be crawled)",
            "competitor_hints": competitor_hints,
        }
        if model:
            request_context["model"] = model

        result = await self._ai_service.generate_structured(
            "research_analysis", request_context, ResearchAnalysisResult
        )
        return result  # type: ignore[no-any-return]


def _build_report(
    report_id: str, company: Company, analysis: ResearchAnalysisResult, *, sources: list[str]
) -> Report:
    resolved_company = dataclasses.replace(company, name=analysis.company_name or company.name)
    competitors = [to_competitor(item, rank=rank) for rank, item in enumerate(analysis.competitors)]
    opportunities = sorted(
        (to_opportunity(item) for item in analysis.growth_opportunities),
        key=lambda opportunity: opportunity.priority_score,
        reverse=True,
    )

    return Report(
        id=report_id,
        company=resolved_company,
        status=ReportStatus.COMPLETE,
        summary=analysis.summary,
        industry=analysis.industry,
        phone=analysis.phone,
        address=analysis.address,
        products=analysis.products,
        services=analysis.services,
        pain_points=analysis.pain_points,
        competitors=competitors,
        opportunities=opportunities,
        sources=list(dict.fromkeys(sources))[:20],
        confidence=analysis.confidence,
        completed_at=utcnow(),
    )
