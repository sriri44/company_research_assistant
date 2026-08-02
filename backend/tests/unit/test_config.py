"""Unit tests for configuration loading/validation (no FastAPI app
involved)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_load_with_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert settings.port == 8000
    assert settings.log_level == "INFO"


def test_settings_uppercase_log_level() -> None:
    settings = Settings(_env_file=None, log_level="debug")

    assert settings.log_level == "DEBUG"


def test_settings_reject_invalid_log_level() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, log_level="NOT_A_LEVEL")


def test_settings_reject_invalid_app_env() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, app_env="not-a-real-env")


def test_settings_reject_out_of_range_port() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, port=70000)
