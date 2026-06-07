from __future__ import annotations

from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from apps.backend.app.modules.educacao.marketplace.search.api.router import get_db, router as search_router


async def fake_get_db():
    yield None


@patch("apps.backend.app.modules.educacao.marketplace.search.api.router.search_engine")
async def test_marketplace_search_route_is_mounted(search_engine_mock):
    app = FastAPI()
    app.include_router(search_router, prefix="/api/v1/educacao/marketplace")

    search_engine_mock.search = AsyncMock(return_value=AsyncMock(items=[]))

    app.dependency_overrides[get_db] = fake_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/api/v1/educacao/marketplace/search/?q=liceu")

    assert response.status_code == 200
    assert response.json()["query"] == "liceu"
    assert response.json()["results"] == []
    search_engine_mock.search.assert_awaited_once()


@patch("apps.backend.app.modules.educacao.marketplace.search.api.router.search_engine")
async def test_marketplace_search_filters_city_slots_price(search_engine_mock):
    app = FastAPI()
    app.include_router(search_router, prefix="/api/v1/educacao/marketplace")

    search_engine_mock.search = AsyncMock(return_value=AsyncMock(items=[]))

    app.dependency_overrides[get_db] = fake_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(
            "/api/v1/educacao/marketplace/search/?q=school&city=Luanda&min_slots=5&price_max=50000&page=2&page_size=50"
        )

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "school"
    assert data["filters_applied"]["city"] == "Luanda"
    assert data["filters_applied"]["min_slots"] == 5
    assert data["filters_applied"]["price_range"] == [None, 50000.0]
    assert data["page"] == 2
    assert data["page_size"] == 50
    search_engine_mock.search.assert_awaited_once()


@patch("apps.backend.app.modules.educacao.marketplace.search.api.router.search_engine")
async def test_marketplace_search_sort_by_quality(search_engine_mock):
    app = FastAPI()
    app.include_router(search_router, prefix="/api/v1/educacao/marketplace")

    search_engine_mock.search = AsyncMock(return_value=AsyncMock(items=[]))

    app.dependency_overrides[get_db] = fake_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.get(
            "/api/v1/educacao/marketplace/search/?q=school&sort_by=quality&page=1&page_size=10"
        )

    assert response.status_code == 200
    data = response.json()
    assert data["sort_by"] == "quality"
    assert data["query"] == "school"
    search_engine_mock.search.assert_awaited_once()

