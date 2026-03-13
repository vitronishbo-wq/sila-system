from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.zona_pesca import ZonaPesca

class ZonaPescaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, zona: ZonaPesca) -> ZonaPesca:
        pass

    @abstractmethod
    async def get_by_id(self, zona_id: UUID) -> ZonaPesca | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> ZonaPesca | None:
        pass

    @abstractmethod
    async def list_ativas(self) -> list[ZonaPesca]:
        pass