from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import StatusVoo
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.voo import Voo

class VooRepositoryPort(ABC):

    @abstractmethod
    async def save(self, voo: Voo) -> Voo:
        ...

    @abstractmethod
    async def get_by_id(self, voo_id: UUID) -> Voo | None:
        ...

    @abstractmethod
    async def get_by_numero(self, numero_voo: str) -> Voo | None:
        ...

    @abstractmethod
    async def list_all(self) -> list[Voo]:
        ...

    @abstractmethod
    async def find_by_status(self, status: StatusVoo) -> list[Voo]:
        ...

    @abstractmethod
    async def find_by_periodo(self, inicio: datetime, fim: datetime) -> list[Voo]:
        ...