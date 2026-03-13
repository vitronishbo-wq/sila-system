from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.resources.ambiente.domain.enums import StatusFiscalizacao
from app.modules.resources.ambiente.domain.models.fiscalizacao import Fiscalizacao

class FiscalizacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Fiscalizacao) -> Fiscalizacao:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_fiscalizacao: str) -> Fiscalizacao | None:
        pass

    @abstractmethod
    async def list(self, *, numero_licenca: str | None=None, status: StatusFiscalizacao | None=None) -> list[Fiscalizacao]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass