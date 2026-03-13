from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusOperacaoUrbana, TipoOperacaoUrbana
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.operacao_urbana import OperacaoUrbana

class OperacaoUrbanaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: OperacaoUrbana) -> OperacaoUrbana:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_operacao: str) -> OperacaoUrbana | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusOperacaoUrbana | None=None, tipo: TipoOperacaoUrbana | None=None, provincia: str | None=None) -> list[OperacaoUrbana]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass