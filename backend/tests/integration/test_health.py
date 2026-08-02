"""Integration tests for the root health/liveness/readiness endpoints.

None of these should ever call an external service — see
docs/ARCHITECTURE.md.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_root_returns_app_info(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["app_name"]
    assert "meta" in body


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_ready_endpoint_returns_ok(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"


def test_health_response_includes_request_id_header(client: TestClient) -> None:
    response = client.get("/health")

    assert "x-request-id" in response.headers
