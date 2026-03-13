from __future__ import annotations
from datetime import datetime
from uuid import UUID
from app.modules.society.patrimonio_cultural.application.ports import CulturalAssetRepositoryPort, TourismServicePort
from app.modules.society.patrimonio_cultural.domain.enums import ActionType, AssetStatus, AssetType, ClassificationLevel
from app.modules.society.patrimonio_cultural.domain.exceptions import AssetAlreadyClassifiedError, AssetNotFoundError, InvalidClassificationAuthorityError
from app.modules.society.patrimonio_cultural.domain.models import CulturalAsset, CulturalEvent, PreservationAction

class CulturalAssetService:
    VALID_AUTHORITIES = {'MinCultura', 'UNESCO', 'Governo Provincial', 'Municipio'}
    LEVEL_ORDER = {ClassificationLevel.MUNICIPAL: 1, ClassificationLevel.PROVINCIAL: 2, ClassificationLevel.NATIONAL: 3, ClassificationLevel.UNESCO: 4, ClassificationLevel.WORLD_HERITAGE: 5}

    def __init__(self, *, asset_repository: CulturalAssetRepositoryPort, tourism_service: TourismServicePort | None=None) -> None:
        self.asset_repository = asset_repository
        self.tourism_service = tourism_service

    async def register_asset(self, *, name: str, asset_type: AssetType, province: str, municipality: str | None=None, latitude: float | None=None, longitude: float | None=None, altitude: float | None=None, address: str | None=None, description: str | None=None, historical_period: str | None=None, cultural_significance: str | None=None, legal_reference: str | None=None) -> CulturalAsset:
        existing = await self.asset_repository.get_by_name_and_province(name=name, province=province)
        if existing:
            raise ValueError(f"Patrimonio '{name}' ja registado na provincia {province}")
        if latitude is not None and (not -90 <= latitude <= 90):
            raise ValueError(f'Latitude invalida: {latitude}')
        if longitude is not None and (not -180 <= longitude <= 180):
            raise ValueError(f'Longitude invalida: {longitude}')
        asset = CulturalAsset(name=name.strip(), asset_type=asset_type, province=province.strip(), municipality=municipality.strip() if municipality else None, latitude=latitude, longitude=longitude, altitude=altitude, address=address, description=description, historical_period=historical_period, cultural_significance=cultural_significance, legal_reference=legal_reference)
        return await self.asset_repository.save(asset)

    async def get_asset_by_id(self, asset_id: UUID) -> CulturalAsset:
        asset = await self.asset_repository.get_by_id(asset_id)
        if asset is None:
            raise AssetNotFoundError(str(asset_id))
        return asset

    async def list_assets(self, *, asset_type: AssetType | None=None, province: str | None=None, classification_level: ClassificationLevel | None=None, status: AssetStatus | None=None, limit: int=100, offset: int=0) -> list[CulturalAsset]:
        return await self.asset_repository.list_by_filters(asset_type=asset_type, province=province, classification_level=classification_level, status=status, limit=limit, offset=offset)

    async def classify_asset(self, *, asset_id: UUID, classification_level: ClassificationLevel, authority: str, classification_date: datetime | None=None) -> CulturalAsset:
        asset = await self.get_asset_by_id(asset_id)
        if authority not in self.VALID_AUTHORITIES:
            raise InvalidClassificationAuthorityError(f"Autoridade '{authority}' nao valida")
        if asset.classification_level is not None:
            current_rank = self.LEVEL_ORDER[asset.classification_level]
            next_rank = self.LEVEL_ORDER[classification_level]
            if next_rank < current_rank:
                raise AssetAlreadyClassifiedError('Nao e possivel reclassificar para nivel inferior')
        asset.classify(level=classification_level, authority=authority, classification_date=classification_date)
        saved = await self.asset_repository.save(asset)
        if self.tourism_service and saved.has_unesco_classification:
            await self.tourism_service.promote_asset(asset_id=saved.asset_id, promotion_data={'name': saved.name, 'classification_level': saved.classification_level.value if saved.classification_level else None})
        return saved

    async def add_preservation_action(self, *, asset_id: UUID, action_type: ActionType, description: str, executed_by: str, action_date: datetime | None=None, cost: float | None=None, funding_source: str | None=None) -> PreservationAction:
        asset = await self.get_asset_by_id(asset_id)
        action = asset.add_preservation_action(action_type=action_type, description=description, executed_by=executed_by, action_date=action_date)
        action.cost = cost
        action.funding_source = funding_source
        saved = await self.asset_repository.save(asset)
        return saved.preservation_actions[-1]

    async def register_cultural_event(self, *, asset_id: UUID, name: str, event_date: datetime, organizer: str, description: str | None=None, expected_attendance: int | None=None, requires_authorization: bool=False) -> CulturalEvent:
        asset = await self.get_asset_by_id(asset_id)
        event = asset.add_event(name=name, event_date=event_date, organizer=organizer)
        event.description = description
        event.expected_attendance = expected_attendance
        event.requires_authorization = requires_authorization
        if asset.is_protected and self.tourism_service:
            await self.tourism_service.promote_asset(asset_id=asset.asset_id, promotion_data={'event_name': name, 'event_date': event_date.isoformat()})
        await self.asset_repository.save(asset)
        return event

    async def get_asset_inventory(self, *, province: str | None=None, classification_level: ClassificationLevel | None=None, include_events: bool=False, include_actions: bool=False) -> list[dict]:
        assets = await self.asset_repository.list_by_filters(province=province, classification_level=classification_level)
        response: list[dict] = []
        for asset in assets:
            data = asset.to_dict()
            if not include_events:
                data.pop('events', None)
            if not include_actions:
                data.pop('preservation_actions', None)
            response.append(data)
        return response

    async def get_protected_assets_report(self, *, province: str | None=None) -> dict:
        assets = await self.asset_repository.list_protected_assets(province=province)
        unesco_assets = [asset for asset in assets if asset.has_unesco_classification]
        return {'total_protected': len(assets), 'by_classification': {level.value: len([a for a in assets if a.classification_level == level]) for level in ClassificationLevel}, 'unesco_count': len(unesco_assets), 'unesco_assets': [asset.to_dict() for asset in unesco_assets], 'by_province': self._group_by_province(assets), 'generated_at': datetime.utcnow().isoformat()}

    @staticmethod
    def _group_by_province(assets: list[CulturalAsset]) -> dict[str, int]:
        grouped: dict[str, int] = {}
        for item in assets:
            province = item.province or 'Nao especificado'
            grouped[province] = grouped.get(province, 0) + 1
        return grouped