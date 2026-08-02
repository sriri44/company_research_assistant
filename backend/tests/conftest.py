"""Shared pytest fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    """A TestClient whose context manager triggers the app's lifespan
    (startup/shutdown), so every request through it exercises the real
    boot sequence."""
    with TestClient(app) as test_client:
        yield test_client
