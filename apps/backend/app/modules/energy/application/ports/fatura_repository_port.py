from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.energy.domain.enums import StatusFaturaEnergia
from apps.backend.app.modules.energy.domain.models import FaturaEnergia


class FaturaRepositoryPort(ABC):
    @abstractmethod
    async def save(self, item: FaturaEnergia) -> FaturaEnergia:
        pass

    @abstractmethod
    async def get_by_id(self, fatura_id: UUID) -> FaturaEnergia | None:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_fatura: str) -> FaturaEnergia | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        unidade_consumidora_id: UUID | None = None,
        cpf_titular: str | None = None,
        status: StatusFaturaEnergia | None = None,
    ) -> list[FaturaEnergia]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass
