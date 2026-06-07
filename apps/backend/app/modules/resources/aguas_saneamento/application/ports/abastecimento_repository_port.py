from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.abastecimento import (
    AbastecimentoAgua,
)


class AbastecimentoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: AbastecimentoAgua) -> AbastecimentoAgua:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_abastecimento: str) -> AbastecimentoAgua | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        infraestrutura_id: UUID | None = None,
        status: StatusAbastecimento | None = None,
        provincia: str | None = None,
        municipio: str | None = None,
    ) -> list[AbastecimentoAgua]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass
