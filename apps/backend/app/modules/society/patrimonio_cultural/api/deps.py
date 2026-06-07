from __future__ import annotations

from uuid import UUID

from apps.backend.app.api.deps import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.patrimonio_cultural.application.ports import (
    TourismServicePort,
)
from apps.backend.app.modules.society.patrimonio_cultural.application.services import (
    CulturalAssetService,
)
from apps.backend.app.modules.society.patrimonio_cultural.infrastructure.repositories import (
    SQLAlchemyCulturalAssetRepository,
)

db_dep = Depends(get_db)


class NullTourismService(TourismServicePort):
    async def promote_asset(self, *, asset_id: UUID, promotion_data: dict) -> bool:
        return True

    async def get_tourist_routes_by_asset(self, *, asset_id: UUID) -> list[dict]:
        return []


async def get_cultural_asset_repository(
    session: AsyncSession = db_dep,
) -> SQLAlchemyCulturalAssetRepository:
    return SQLAlchemyCulturalAssetRepository(session)


async def get_tourism_service() -> TourismServicePort:
    return NullTourismService()


cultural_asset_repository_dep = Depends(get_cultural_asset_repository)
tourism_service_dep = Depends(get_tourism_service)


async def get_cultural_asset_service(
    repository: SQLAlchemyCulturalAssetRepository = cultural_asset_repository_dep,
    tourism_service: TourismServicePort = tourism_service_dep,
) -> CulturalAssetService:
    return CulturalAssetService(asset_repository=repository, tourism_service=tourism_service)