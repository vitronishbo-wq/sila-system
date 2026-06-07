from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from apps.backend.app.modules.educacao.marketplace.matching.api.router import get_db, router as matching_router


class FakeInstitutionModel:
    institution_id = "inst-1"
    name = "Liceu Teste"
    type = "privada"
    province = "Luanda"
    municipality = "Luanda"
    district = "Maianga"
    available_slots = 10
    monthly_fee_avg = 15000.0
    rating = 4.2
    approval_rate = 0.95
    average_academic_performance = 78.0
    specializations = ["Matemática", "Ciências"]
    supports_special_needs = True
    special_needs_types = ["deficiência motora"]
    teaching_modalities = ["presencial"]
    transfer_acceptance_rate = 0.9
    is_active = True


class FakeResult:
    def __init__(self, item):
        self._item = item

    def scalars(self):
        return self

    def all(self):
        return [self._item]

    def scalar_one_or_none(self):
        return self._item


async def fake_get_db():
    session = Mock()
    session.execute = AsyncMock(return_value=FakeResult(FakeInstitutionModel()))
    yield session


@patch("apps.backend.app.modules.educacao.marketplace.matching.api.router.recommendation_engine")
async def test_matching_recommendations_route(recommendation_engine_mock):
    app = FastAPI()
    app.include_router(matching_router, prefix="/api/v1/educacao")
    app.dependency_overrides[get_db] = fake_get_db

    recommendation = Mock(
        primary_match=Mock(
            institution_id="inst-1",
            institution_name="Liceu Teste",
            match_score=92.5,
            compatibility_score=90.0,
            ranking_position=1,
            reasons=["Muito próxima", "Boa qualidade"],
            match_factors={"distance": 90.0, "quality": 92.5},
        ),
        alternative_matches=[
            Mock(
                institution_id="inst-1",
                institution_name="Liceu Alternativa",
                match_score=85.0,
                compatibility_score=82.0,
                ranking_position=2,
                reasons=["Boa localização"],
                match_factors={"distance": 85.0, "quality": 80.0},
            )
        ],
        reasoning="A melhor opção baseada no seu perfil.",
        suggested_actions=["Aplique rápido", "Prepare documentos"],
        timeline="Admissão em 4 semanas",
        success_probability=0.88,
    )

    recommendation_engine_mock.generate_recommendation = AsyncMock(return_value=recommendation)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        response = await client.post(
            "/api/v1/educacao/marketplace/matching/recommendations",
            json={
                "student_id": "stu-1",
                "age": 17,
                "academic_performance": 80.0,
                "special_needs": [],
                "location": {"province": "Luanda", "municipality": "Luanda", "district": "Maianga"},
                "available_budget": 20000.0,
                "preferred_modalities": ["presencial"],
                "educational_level": "secundario",
                "previous_transfers": 0,
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "stu-1"
    assert data["recommended_institution"]["institution_id"] == "inst-1"
    assert data["success_probability"] == 0.88
    recommendation_engine_mock.generate_recommendation.assert_awaited_once()
