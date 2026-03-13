from __future__ import annotations
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.society.patrimonio_cultural.api.deps import get_cultural_asset_service
from app.modules.society.patrimonio_cultural.api.router import router as patrimonio_cultural_router
from app.modules.society.patrimonio_cultural.application.services import CulturalAssetService
from app.modules.society.patrimonio_cultural.tests._fakes import FakeTourismService, InMemoryCulturalAssetRepository

def _build_client() -> TestClient:
    app = FastAPI()
    app.include_router(patrimonio_cultural_router)
    service = CulturalAssetService(asset_repository=InMemoryCulturalAssetRepository(), tourism_service=FakeTourismService())
    app.dependency_overrides[get_cultural_asset_service] = lambda: service
    return TestClient(app)

def test_patrimonio_lifecycle_e2e() -> None:
    client = _build_client()
    register_payload = {'name': 'Museu Nacional de Antropologia', 'asset_type': 'museum_collection', 'province': 'Luanda', 'municipality': 'Ingombota', 'latitude': -8.815, 'longitude': 13.232, 'historical_period': 'Seculo XX', 'description': 'Principal museu de antropologia de Angola'}
    response = client.post('/patrimonio-cultural/assets/', json=register_payload)
    assert response.status_code == 201
    asset = response.json()
    asset_id = asset['asset_id']
    classify_payload = {'classification_level': 'national', 'authority': 'MinCultura'}
    response = client.post(f'/patrimonio-cultural/assets/{asset_id}/classification', json=classify_payload)
    assert response.status_code == 200
    assert response.json()['classification_level'] == 'national'
    assert response.json()['is_protected'] is True
    action_payload = {'action_type': 'conservation', 'description': 'Restauro de fachada principal e sistema de climatizacao', 'executed_by': 'Instituto do Patrimonio Cultural', 'cost': 150000.0, 'funding_source': 'Orcamento do Estado'}
    response = client.post(f'/patrimonio-cultural/assets/{asset_id}/preservation-actions', json=action_payload)
    assert response.status_code == 201
    event_payload = {'name': 'Exposicao Temporaria: Culturas Bantu', 'event_date': '2026-06-15T10:00:00Z', 'organizer': 'Ministerio da Cultura', 'expected_attendance': 500, 'requires_authorization': True}
    response = client.post(f'/patrimonio-cultural/assets/{asset_id}/events', json=event_payload)
    assert response.status_code == 201
    response = client.get('/patrimonio-cultural/assets/inventory', params={'province': 'Luanda', 'include_events': True})
    assert response.status_code == 200
    inventory = response.json()
    assert len(inventory) >= 1
    assert any((item['asset_id'] == asset_id for item in inventory))
    response = client.get('/patrimonio-cultural/assets/protected/report')
    assert response.status_code == 200
    report = response.json()
    assert report['total_protected'] >= 1
    assert 'unesco_count' in report