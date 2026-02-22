# tests/modules/location/test_location_endpoints.py
"""
Location Module Endpoint Tests
Tests the location API endpoints in isolation using mocks.
"""
from apps.backend.core.db.session import get_db
from apps.backend.main import app
import sys
import os
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from fastapi import status
from httpx import AsyncClient, ASGITransport

# Setup path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
sys.path.insert(0, project_root)


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def client_with_mock_db(async_client, monkeypatch):
    """Override get_db with a mock session."""
    mock_session = AsyncMock()

    async def mock_get_db():
        yield mock_session

    monkeypatch.setattr("apps.backend.core.db.session.get_db", mock_get_db)
    yield async_client


@pytest.mark.asyncio
async def test_location_ping(client_with_mock_db: AsyncClient):
    response = await client_with_mock_db.get("/location/ping")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_list_provinces(client_with_mock_db: AsyncClient, monkeypatch):
    mock_province = type("Province", (), {"id": 1, "name": "Luanda"})
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = [mock_province]
    mock_result.scalars.return_value = mock_scalars

    async def mock_execute(*args, **kwargs):
        return mock_result

    monkeypatch.setattr(
        "apps.backend.modules.location.services.location_service.AsyncSession.execute", mock_execute)

    response = await client_with_mock_db.get("/location/provinces")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Luanda"


@pytest.mark.asyncio
async def test_list_municipalities(client_with_mock_db: AsyncClient, monkeypatch):
    mock_municipality = type("Municipality", (), {"id": 1, "name": "Belas"})
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = [mock_municipality]
    mock_result.scalars.return_value = mock_scalars

    async def mock_execute(*args, **kwargs):
        return mock_result

    monkeypatch.setattr(
        "apps.backend.modules.location.services.location_service.AsyncSession.execute", mock_execute)

    response = await client_with_mock_db.get("/location/municipalities")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Belas"


@pytest.mark.asyncio
async def test_list_communes(client_with_mock_db: AsyncClient, monkeypatch):
    mock_commune = type("Commune", (), {"id": 1, "name": "Sambizanga"})
    mock_result = AsyncMock()
    mock_scalars = AsyncMock()
    mock_scalars.all.return_value = [mock_commune]
    mock_result.scalars.return_value = mock_scalars

    async def mock_execute(*args, **kwargs):
        return mock_result

    monkeypatch.setattr(
        "apps.backend.modules.location.services.location_service.AsyncSession.execute", mock_execute)

    response = await client_with_mock_db.get("/location/communes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Sambizanga"


@pytest.mark.asyncio
async def test_invalid_endpoint_returns_404(client_with_mock_db: AsyncClient):
    response = await client_with_mock_db.get("/location/invalid")
    assert response.status_code == status.HTTP_404_NOT_FOUND
