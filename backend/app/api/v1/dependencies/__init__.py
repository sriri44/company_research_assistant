"""FastAPI Depends() providers.

One function per service interface (`get_company_service`,
`get_search_service`, `get_crawler_service`, `get_ai_service`,
`get_competitor_service`, `get_opportunity_service`, `get_report_service`,
`get_discord_service`), plus `get_current_settings`. Each delegates to
`app.core.container.get_container()`, which owns construction. Routes
depend only on these providers, never on implementations or the container
directly.
"""
