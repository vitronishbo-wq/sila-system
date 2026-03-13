from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLoteamento, TipoLoteamento
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.loteamento import Loteamento

class LoteamentoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Loteamento) -> Loteamento:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_loteamento: str) -> Loteamento | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusLoteamento | None=None, tipo: TipoLoteamento | None=None, provincia: str | None=None) -> list[Loteamento]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass