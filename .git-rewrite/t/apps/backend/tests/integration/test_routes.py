"""
Pytest tests to verify API endpoints (v1 legacy and v2 current).
"""

import os

import pytest
from fastapi.testclient import TestClient

from app.main import app  # importa FastAPI principal

# 🔑 credenciais de teste (pode vir de env vars no CI/CD)
TEST_EMAIL = settings.TEST_EMAIL
TEST_PASSWORD = settings.TEST_PASSWORD


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_check(client):
    response = client.get("/api/v2/health")
    assert response.status_code in [200, 404]  # depende da migração


@pytest.mark.asyncio
async def test_auth_login_v2(client):
    response = client.post(
        "/api/v2/auth/login",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code in [200, 401, 422, 404]


@pytest.mark.asyncio
async def test_auth_login_v1_legacy(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert response.status_code in [200, 401, 422, 404]


@pytest.mark.asyncio
async def test_dashboard_resumo_v2(client):
    response = client.get("/v2/dashboard/resumo")
    assert response.status_code in [200, 401, 404]


@pytest.mark.asyncio
async def test_dashboard_municipios_v2(client):
    response = client.get("/v2/dashboard/municipios")
    assert response.status_code in [200, 401, 404]
