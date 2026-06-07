from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.florestas.domain.models.concessionario_florestal import (
    ConcessionarioFlorestal,
)


class ConcessionarioFlorestalRepositoryPort(ABC):
    @abstractmethod
    async def save(self, operador: ConcessionarioFlorestal) -> ConcessionarioFlorestal:
        pass

    @abstractmethod
    async def get_by_id(self, operador_id: UUID) -> ConcessionarioFlorestal | None:
        pass

    @abstractmethod
    async def get_by_nif(self, nif: str) -> ConcessionarioFlorestal | None:
        pass

    @abstractmethod
    async def list_all(self, ativo: bool | None = None) -> list[ConcessionarioFlorestal]:
        pass
