from __future__ import annotations

import os

os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379")

from unittest.mock import Mock, patch

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from apps.backend.app.modules.educacao.api.vacancies_router import router as vacancies_router


async def test_vacancies_endpoint_returns_real_marketplace_data() -> None:
    app = FastAPI()
    app.include_router(vacancies_router, prefix="/api/v1/educacao")

    fake_vacancies = [
        {"institution": "school-abc", "grade": "9", "available_slots": 3}
    ]

    with patch(
        "apps.backend.app.modules.educacao.api.vacancies_router.VacancyMarketplace"
    ) as marketplace_cls:
        marketplace = Mock()
        marketplace.list_vacancies.return_value = fake_vacancies
        marketplace_cls.return_value = marketplace

        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
        ) as client:
            response = await client.get(
                "/api/v1/educacao/vacancies/?institution_id=school-abc&class_name=9"
            )

    assert response.status_code == 200
    assert response.json() == fake_vacancies
    marketplace.list_vacancies.assert_called_once_with(
        {
            "institution_id": "school-abc",
            "class_name": "9",
            "academic_year": None,
        }
    )
