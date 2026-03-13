from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusOneracao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.oneracao import Oneracao

class OneracaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Oneracao) -> Oneracao:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_oneracao: str) -> Oneracao | None:
        pass

    @abstractmethod
    async def list(self, *, imovel_inscricao: str | None=None, status: StatusOneracao | None=None, ativo: bool | None=None) -> list[Oneracao]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass