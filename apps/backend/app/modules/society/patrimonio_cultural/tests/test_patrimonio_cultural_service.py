from __future__ import annotations
import asyncio
import pytest
from apps.backend.app.modules.society.patrimonio_cultural.application.services import CulturalAssetService
from apps.backend.app.modules.society.patrimonio_cultural.domain.enums import ActionType, AssetType, ClassificationLevel
from apps.backend.app.modules.society.patrimonio_cultural.domain.exceptions import UNESCOPreconditionError
from apps.backend.app.modules.society.patrimonio_cultural.tests._fakes import FakeTourismService, InMemoryCulturalAssetRepository

def test_patrimonio_cultural_lifecycle_service() -> None:

    async def scenario() -> None:
        tourism = FakeTourismService()
        service = CulturalAssetService(asset_repository=InMemoryCulturalAssetRepository(), tourism_service=tourism)
        asset = await service.register_asset(name='Fortaleza de Sao Miguel', asset_type=AssetType.MONUMENT, province='Luanda', municipality='Ingombota', latitude=-8.8089, longitude=13.2344, historical_period='Seculo XVII')
        assert asset.status.value == 'registered'
        asset = await service.classify_asset(asset_id=asset.asset_id, classification_level=ClassificationLevel.NATIONAL, authority='MinCultura')
        assert asset.is_protected is True
        assert asset.classification_level == ClassificationLevel.NATIONAL
        action = await service.add_preservation_action(asset_id=asset.asset_id, action_type=ActionType.CONSERVATION, description='Consolidacao estrutural e limpeza tecnica da fachada', executed_by='Instituto Nacional do Patrimonio', cost=120000.0)
        assert action.action_type == ActionType.CONSERVATION
        event = await service.register_cultural_event(asset_id=asset.asset_id, name='Jornada de Educacao Patrimonial', event_date=asset.created_at, organizer='Ministerio da Cultura', expected_attendance=300)
        assert event.name == 'Jornada de Educacao Patrimonial'
        inventory = await service.get_asset_inventory(province='Luanda', include_events=True, include_actions=True)
        assert len(inventory) == 1
        assert len(inventory[0]['events']) == 1
        assert len(inventory[0]['preservation_actions']) == 1
        report = await service.get_protected_assets_report(province='Luanda')
        assert report['total_protected'] == 1
        assert report['unesco_count'] == 0
        assert report['by_province']['Luanda'] == 1
    asyncio.run(scenario())

def test_unesco_requires_national_first() -> None:

    async def scenario() -> None:
        service = CulturalAssetService(asset_repository=InMemoryCulturalAssetRepository(), tourism_service=FakeTourismService())
        asset = await service.register_asset(name='Sitio Arqueologico A', asset_type=AssetType.ARCHAEOLOGICAL_SITE, province='Bie')
        with pytest.raises(UNESCOPreconditionError):
            await service.classify_asset(asset_id=asset.asset_id, classification_level=ClassificationLevel.UNESCO, authority='UNESCO')
    asyncio.run(scenario())