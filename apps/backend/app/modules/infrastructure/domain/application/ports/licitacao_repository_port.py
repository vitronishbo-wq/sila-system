from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao
from apps.backend.app.modules.infrastructure.domain.models.licitacao import Licitacao

class LicitacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Licitacao) -> Licitacao:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_licitacao: str) -> Licitacao | None:
        pass

    @abstractmethod
    async def list(self, *, status: StatusLicitacao | None=None, tipo: TipoLicitacao | None=None, obra_id: UUID | None=None, orgao_responsavel_id: UUID | None=None) -> list[Licitacao]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass
