from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusConsumo
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.consumo_agua import ConsumoAgua

class ConsumoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: ConsumoAgua) -> ConsumoAgua:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_consumo: str) -> ConsumoAgua | None:
        pass

    @abstractmethod
    async def list(self, *, abastecimento_id: UUID | None=None, titular_id: UUID | None=None, referencia: str | None=None, status: StatusConsumo | None=None) -> list[ConsumoAgua]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass