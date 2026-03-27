"""Smoke tests for placeholder FastAPI routes (VETES-16)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "enae-vet-es-api"


def test_swagger_ui_available() -> None:
    response = client.get("/docs")
    assert response.status_code == 200
    assert b"swagger" in response.content.lower()


def test_openapi_json_lists_paths() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    assert "/health" in body.get("paths", {})
    assert "/api/v1/echo" in body.get("paths", {})


def test_echo_placeholder_round_trip() -> None:
    response = client.post("/api/v1/echo", json={"text": "ping"})
    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "echo:ping"
    assert data["placeholder"] is True
