from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class TourismServicePort(ABC):

    @abstractmethod
    async def promote_asset(self, *, asset_id: UUID, promotion_data: dict) -> bool:
        pass

    @abstractmethod
    async def get_tourist_routes_by_asset(self, *, asset_id: UUID) -> list[dict]:
        pass