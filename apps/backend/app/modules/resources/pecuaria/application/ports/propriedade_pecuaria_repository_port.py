from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.pecuaria.domain.models.propriedade_pecuaria import (
    PropriedadePecuaria,
)


class PropriedadePecuariaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: PropriedadePecuaria) -> PropriedadePecuaria:
        pass

    @abstractmethod
    async def get_by_id(self, propriedade_id: UUID) -> PropriedadePecuaria | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_propriedade: str) -> PropriedadePecuaria | None:
        pass

    @abstractmethod
    async def list_by_pecuarista(
        self, pecuarista_id: UUID | None = None
    ) -> list[PropriedadePecuaria]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
