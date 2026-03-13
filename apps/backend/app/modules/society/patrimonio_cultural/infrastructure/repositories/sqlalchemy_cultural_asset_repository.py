from __future__ import annotations
from uuid import UUID
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.patrimonio_cultural.application.ports import CulturalAssetRepositoryPort
from app.modules.society.patrimonio_cultural.domain.enums import AssetStatus, AssetType, ClassificationLevel
from app.modules.society.patrimonio_cultural.domain.models import CulturalAsset
from app.modules.society.patrimonio_cultural.infrastructure.models import CulturalAssetModel

class SQLAlchemyCulturalAssetRepository(CulturalAssetRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, asset: CulturalAsset) -> CulturalAsset:
        model = await self.session.get(CulturalAssetModel, asset.asset_id)
        if not model:
            model = CulturalAssetModel(asset_id=asset.asset_id)
            self.session.add(model)
        model.name = asset.name
        model.asset_type = asset.asset_type.value
        model.description = asset.description
        model.latitude = asset.latitude
        model.longitude = asset.longitude
        model.altitude = asset.altitude
        model.province = asset.province
        model.municipality = asset.municipality
        model.address = asset.address
        model.status = asset.status.value
        model.classification_level = asset.classification_level.value if asset.classification_level else None
        model.classification_date = asset.classification_date
        model.historical_period = asset.historical_period
        model.cultural_significance = asset.cultural_significance
        model.legal_reference = asset.legal_reference
        model.classifications = [item.to_dict() for item in asset.classifications]
        model.events = [item.to_dict() for item in asset.events]
        model.preservation_actions = [item.to_dict() for item in asset.preservation_actions]
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, asset_id: UUID) -> CulturalAsset | None:
        model = await self.session.get(CulturalAssetModel, asset_id)
        return self._to_domain(model) if model else None

    async def get_by_name_and_province(self, *, name: str, province: str) -> CulturalAsset | None:
        stmt = select(CulturalAssetModel).where(and_(CulturalAssetModel.name == name.strip(), CulturalAssetModel.province == province.strip()))
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_filters(self, *, asset_type: AssetType | None=None, province: str | None=None, classification_level: ClassificationLevel | None=None, status: AssetStatus | None=None, limit: int=100, offset: int=0) -> list[CulturalAsset]:
        stmt = select(CulturalAssetModel)
        if asset_type:
            stmt = stmt.where(CulturalAssetModel.asset_type == asset_type.value)
        if province:
            stmt = stmt.where(CulturalAssetModel.province.ilike(f'%{province.strip()}%'))
        if classification_level:
            stmt = stmt.where(CulturalAssetModel.classification_level == classification_level.value)
        if status:
            stmt = stmt.where(CulturalAssetModel.status == status.value)
        stmt = stmt.order_by(CulturalAssetModel.name.asc()).limit(limit).offset(offset)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(model) for model in models]

    async def list_protected_assets(self, *, province: str | None=None) -> list[CulturalAsset]:
        stmt = select(CulturalAssetModel).where(CulturalAssetModel.status == AssetStatus.PROTECTED.value)
        if province:
            stmt = stmt.where(CulturalAssetModel.province == province.strip())
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(model) for model in models]

    async def list_unesco_assets(self) -> list[CulturalAsset]:
        stmt = select(CulturalAssetModel).where(CulturalAssetModel.classification_level.in_([ClassificationLevel.UNESCO.value, ClassificationLevel.WORLD_HERITAGE.value]))
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(model) for model in models]

    @staticmethod
    def _to_domain(model: CulturalAssetModel) -> CulturalAsset:
        data = {'asset_id': str(model.asset_id), 'name': model.name, 'asset_type': model.asset_type, 'description': model.description, 'latitude': model.latitude, 'longitude': model.longitude, 'altitude': model.altitude, 'province': model.province, 'municipality': model.municipality, 'address': model.address, 'status': model.status, 'classification_level': model.classification_level, 'classification_date': model.classification_date.isoformat() if model.classification_date else None, 'historical_period': model.historical_period, 'cultural_significance': model.cultural_significance, 'legal_reference': model.legal_reference, 'created_at': model.created_at.isoformat(), 'updated_at': model.updated_at.isoformat() if model.updated_at else None, 'classifications': model.classifications or [], 'events': model.events or [], 'preservation_actions': model.preservation_actions or []}
        return CulturalAsset.from_dict(data)