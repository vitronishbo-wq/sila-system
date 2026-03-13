from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusCAR
from apps.backend.app.modules.resources.ambiente.domain.models.car import CAR

class CARRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: CAR) -> CAR:
        pass

    @abstractmethod
    async def get_by_id(self, car_id: UUID) -> CAR | None:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_car: str) -> CAR | None:
        pass

    @abstractmethod
    async def get_by_imovel(self, imovel_id: UUID) -> CAR | None:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusCAR | None=None) -> list[CAR]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass