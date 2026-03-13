from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.ambiente.application.ports.car_repository_port import CARRepositoryPort
from app.modules.resources.ambiente.domain.enums import StatusCAR
from app.modules.resources.ambiente.domain.models.car import CAR

class SQLAlchemyCARRepository(CARRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, CAR] = {}
        self._seq = 0

    async def save(self, item: CAR) -> CAR:
        self._items[item.id] = item
        return item

    async def get_by_id(self, car_id: UUID) -> CAR | None:
        return self._items.get(car_id)

    async def get_by_numero(self, numero_car: str) -> CAR | None:
        for item in self._items.values():
            if item.numero_car == numero_car:
                return item
        return None

    async def get_by_imovel(self, imovel_id: UUID) -> CAR | None:
        for item in self._items.values():
            if item.imovel_id == imovel_id:
                return item
        return None

    async def list_by_status(self, status: StatusCAR | None=None) -> list[CAR]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def next_numero(self) -> str:
        self._seq += 1
        return f'CAR/{date.today().year}/{self._seq:06d}'