from __future__ import annotations
from uuid import UUID
from app.modules.society.patrimonio_cultural.application.ports import CulturalAssetRepositoryPort, TourismServicePort
from app.modules.society.patrimonio_cultural.domain.enums import AssetStatus, AssetType, ClassificationLevel
from app.modules.society.patrimonio_cultural.domain.models import CulturalAsset

class InMemoryCulturalAssetRepository(CulturalAssetRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, CulturalAsset] = {}

    async def save(self, asset: CulturalAsset) -> CulturalAsset:
        self._items[asset.asset_id] = asset
        return asset

    async def get_by_id(self, asset_id: UUID) -> CulturalAsset | None:
        return self._items.get(asset_id)

    async def get_by_name_and_province(self, *, name: str, province: str) -> CulturalAsset | None:
        expected_name = name.strip().lower()
        expected_province = province.strip().lower()
        for item in self._items.values():
            if item.name.lower() == expected_name and (item.province or '').lower() == expected_province:
                return item
        return None

    async def list_by_filters(self, *, asset_type: AssetType | None=None, province: str | None=None, classification_level: ClassificationLevel | None=None, status: AssetStatus | None=None, limit: int=100, offset: int=0) -> list[CulturalAsset]:
        items = list(self._items.values())
        if asset_type:
            items = [item for item in items if item.asset_type == asset_type]
        if province:
            province_normalized = province.strip().lower()
            items = [item for item in items if province_normalized in (item.province or '').lower()]
        if classification_level:
            items = [item for item in items if item.classification_level == classification_level]
        if status:
            items = [item for item in items if item.status == status]
        items = sorted(items, key=lambda item: item.name)
        return items[offset:offset + limit]

    async def list_protected_assets(self, *, province: str | None=None) -> list[CulturalAsset]:
        items = [item for item in self._items.values() if item.status == AssetStatus.PROTECTED]
        if province:
            province_normalized = province.strip().lower()
            items = [item for item in items if (item.province or '').lower() == province_normalized]
        return sorted(items, key=lambda item: item.name)

    async def list_unesco_assets(self) -> list[CulturalAsset]:
        items = [item for item in self._items.values() if item.has_unesco_classification]
        return sorted(items, key=lambda item: item.name)

class FakeTourismService(TourismServicePort):

    def __init__(self) -> None:
        self.promotions: list[dict] = []

    async def promote_asset(self, *, asset_id: UUID, promotion_data: dict) -> bool:
        self.promotions.append({'asset_id': str(asset_id), 'data': promotion_data})
        return True

    async def get_tourist_routes_by_asset(self, *, asset_id: UUID) -> list[dict]:
        return []