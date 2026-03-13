from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.models.fiscalizacao_pesca import FiscalizacaoPesca

class FiscalizacaoPescaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: FiscalizacaoPesca) -> FiscalizacaoPesca:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> FiscalizacaoPesca | None:
        pass

    @abstractmethod
    async def list_by_embarcacao(self, embarcacao_id: UUID) -> list[FiscalizacaoPesca]:
        pass

    @abstractmethod
    async def list_irregularidades(self) -> list[FiscalizacaoPesca]:
        pass