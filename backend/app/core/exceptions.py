"""Domain exception taxonomy.

Every service raises one of these (never a bare `Exception` or
`HTTPException`) so `app.middleware.error_handler` can translate any
failure into the standard error envelope (docs/ARCHITECTURE.md §11) with a
stable, machine-readable `code`.
"""

from __future__ import annotations


class AppError(Exception):
    """Base class for all domain exceptions."""

    code: str = "INTERNAL_ERROR"
    http_status: int = 500

    def __init__(self, message: str, details: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or []


class CompanyNotFoundError(AppError):
    code = "COMPANY_NOT_FOUND"
    http_status = 404


class SearchProviderError(AppError):
    code = "SEARCH_PROVIDER_ERROR"
    http_status = 502


class CrawlerError(AppError):
    code = "CRAWLER_ERROR"
    http_status = 502


class AIProviderError(AppError):
    code = "AI_PROVIDER_ERROR"
    http_status = 502


class ReportNotFoundError(AppError):
    code = "REPORT_NOT_FOUND"
    http_status = 404


class ReportGenerationError(AppError):
    code = "REPORT_GENERATION_FAILED"
    http_status = 500


class DiscordDeliveryError(AppError):
    code = "DISCORD_DELIVERY_FAILED"
    http_status = 502
