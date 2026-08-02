"""Dependency injection container.

Constructs and holds the single instance of each service implementation
for the lifetime of the application. `app.api.v1.dependencies` exposes
these to routes via FastAPI's `Depends()`; nothing outside this module
should construct a service implementation directly.

One `AsyncHttpClient` is shared by `SerperClient` and `OpenRouterClient`
(one connection-pooled httpx client for the whole process, per the
"reuse HTTP client" performance requirement) — everything downstream of
it is wired from real, non-placeholder implementations as of this phase.
`DiscordService` remains a placeholder; Discord delivery is a later phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from app.ai.openrouter_client import OpenRouterClient
from app.clients.http_client import AsyncHttpClient
from app.core.config import get_settings
from app.search.serper_client import SerperClient
from app.services.implementations.ai_competitor_service import AICompetitorService
from app.services.implementations.ai_opportunity_service import AIOpportunityService
from app.services.implementations.crawl4ai_crawler_service import Crawl4AICrawlerService
from app.services.implementations.default_company_service import DefaultCompanyService
from app.services.implementations.openrouter_ai_service import OpenRouterAIService
from app.services.implementations.placeholder_discord_service import PlaceholderDiscordService
from app.services.implementations.research_report_service import ResearchReportService
from app.services.implementations.serper_search_service import SerperSearchService
from app.services.interfaces.ai_service import AIService
from app.services.interfaces.company_service import CompanyService
from app.services.interfaces.competitor_service import CompetitorService
from app.services.interfaces.crawler_service import CrawlerService
from app.services.interfaces.discord_service import DiscordService
from app.services.interfaces.opportunity_service import OpportunityService
from app.services.interfaces.report_service import ReportService
from app.services.interfaces.search_service import SearchService


@dataclass(frozen=True)
class Container:
    company_service: CompanyService
    search_service: SearchService
    crawler_service: CrawlerService
    ai_service: AIService
    competitor_service: CompetitorService
    opportunity_service: OpportunityService
    report_service: ReportService
    research_report_service: ResearchReportService
    discord_service: DiscordService


@lru_cache
def get_container() -> Container:
    """Build (once) and return the application's service container."""
    settings = get_settings()

    http_client = AsyncHttpClient(
        timeout=settings.request_timeout,
        max_retries=settings.http_max_retries,
        backoff_seconds=settings.http_retry_backoff_seconds,
    )

    serper_client = SerperClient(settings.serper_api_key, settings.serper_base_url, http_client)
    openrouter_client = OpenRouterClient(
        settings.openrouter_api_key, settings.openrouter_base_url, http_client
    )

    search_service = SerperSearchService(serper_client)
    crawler_service = Crawl4AICrawlerService(
        user_agent=settings.user_agent,
        max_pages=settings.max_crawl_pages,
        page_timeout_seconds=settings.request_timeout,
    )
    ai_service = OpenRouterAIService(openrouter_client, settings.openrouter_default_model)
    company_service = DefaultCompanyService(search_service)
    competitor_service = AICompetitorService(search_service, ai_service)
    opportunity_service = AIOpportunityService(ai_service)
    research_report_service = ResearchReportService(
        company_service,
        search_service,
        crawler_service,
        ai_service,
        max_context_words=settings.max_context_words,
    )

    return Container(
        company_service=company_service,
        search_service=search_service,
        crawler_service=crawler_service,
        ai_service=ai_service,
        competitor_service=competitor_service,
        opportunity_service=opportunity_service,
        report_service=research_report_service,
        research_report_service=research_report_service,
        discord_service=PlaceholderDiscordService(),
    )
