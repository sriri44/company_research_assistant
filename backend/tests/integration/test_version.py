"""Integration test for the root /version endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_version_endpoint_returns_app_metadata(client: TestClient) -> None:
    response = client.get("/version")

    assert response.status_code == 200
    data = response.json()["data"]
    assert "app_version" in data
    assert "app_env" in data
    assert data["app_env"] in {"development", "staging", "production", "test"}
