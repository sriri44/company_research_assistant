"""Verifies the application boots and shuts down cleanly via its lifespan.

`TestClient` used as a context manager triggers FastAPI's lifespan
startup/shutdown, so this exercises configuration loading, logging setup,
and dependency container construction end to end.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_app_starts_and_serves_requests() -> None:
    with TestClient(app) as test_client:
        response = test_client.get("/health")
        assert response.status_code == 200


def test_app_exposes_versioned_api_surface() -> None:
    with TestClient(app) as test_client:
        response = test_client.post("/api/v1/company/resolve")
        assert response.status_code == 501
        assert response.json()["success"] is False
        assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"
