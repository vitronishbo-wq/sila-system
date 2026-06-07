from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    StatusInfraestrutura,
    TipoInfraestrutura,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.infraestrutura import (
    InfraestruturaHidrica,
)


class InfraestruturaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: InfraestruturaHidrica) -> InfraestruturaHidrica:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_infraestrutura: str) -> InfraestruturaHidrica | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        tipo: TipoInfraestrutura | None = None,
        status: StatusInfraestrutura | None = None,
        provincia: str | None = None,
        municipio: str | None = None,
    ) -> list[InfraestruturaHidrica]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
