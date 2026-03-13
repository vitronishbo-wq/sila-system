from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.patrimonio_cultural.domain.enums import AssetStatus, AssetType, ClassificationLevel
from app.modules.society.patrimonio_cultural.domain.models import CulturalAsset

class CulturalAssetRepositoryPort(ABC):

    @abstractmethod
    async def save(self, asset: CulturalAsset) -> CulturalAsset:
        pass

    @abstractmethod
    async def get_by_id(self, asset_id: UUID) -> CulturalAsset | None:
        pass

    @abstractmethod
    async def get_by_name_and_province(self, *, name: str, province: str) -> CulturalAsset | None:
        pass

    @abstractmethod
    async def list_by_filters(self, *, asset_type: AssetType | None=None, province: str | None=None, classification_level: ClassificationLevel | None=None, status: AssetStatus | None=None, limit: int=100, offset: int=0) -> list[CulturalAsset]:
        pass

    @abstractmethod
    async def list_protected_assets(self, *, province: str | None=None) -> list[CulturalAsset]:
        pass

    @abstractmethod
    async def list_unesco_assets(self) -> list[CulturalAsset]:
        pass