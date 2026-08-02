"""Application settings.

Single source of truth for environment-driven configuration. No module
outside this file should read `os.environ` directly — everything flows
through the `Settings` instance, constructed once (via `get_settings`) and
provided via DI (`app.core.container`, `app.api.v1.dependencies`).

Field values mirror `backend/.env.example`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_VALID_APP_ENVS = {"development", "staging", "production", "test"}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App identity
    app_name: str = "AI Company Research Assistant API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)

    # API surface (supports the routers/middleware built in this phase)
    api_prefix: str = "/api/v1"
    cors_allowed_origins: list[str] = ["http://localhost:5173"]
    allowed_hosts: list[str] = ["*"]

    # Search — Serper.dev
    serper_api_key: str = ""
    serper_base_url: str = "https://google.serper.dev"

    # AI — OpenRouter
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_default_model: str = "openai/gpt-4o-mini"

    # Discord
    discord_token: str = ""
    discord_channel: str = ""

    # Logging
    log_level: str = "INFO"

    # PDF
    pdf_output_path: str = "./generated_reports"

    # Crawler / outbound HTTP
    max_crawl_pages: int = Field(default=10, gt=0, le=10)
    request_timeout: int = Field(default=30, gt=0)
    user_agent: str = "CompanyResearchAssistant/1.0"

    # Resilience (shared by SerperClient/OpenRouterClient/Crawl4AI wrapper)
    http_max_retries: int = Field(default=3, ge=1, le=10)
    http_retry_backoff_seconds: float = Field(default=0.75, gt=0)
    ai_request_timeout: int = Field(default=60, gt=0)
    max_context_words: int = Field(default=12_000, gt=0)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        upper = value.upper()
        if upper not in _VALID_LOG_LEVELS:
            raise ValueError(f"log_level must be one of {sorted(_VALID_LOG_LEVELS)}, got {value!r}")
        return upper

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, value: str) -> str:
        lower = value.lower()
        if lower not in _VALID_APP_ENVS:
            raise ValueError(f"app_env must be one of {sorted(_VALID_APP_ENVS)}, got {value!r}")
        return lower


@lru_cache
def get_settings() -> Settings:
    """Return the cached `Settings` instance, constructing it once."""
    return Settings()
