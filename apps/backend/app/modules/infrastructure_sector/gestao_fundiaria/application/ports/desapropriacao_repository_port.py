from __future__ import annotations
from abc import ABC, abstractmethod
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusDesapropriacao
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.desapropriacao import Desapropriacao

class DesapropriacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Desapropriacao) -> Desapropriacao:
        pass

    @abstractmethod
    async def get_by_numero_processo(self, numero_processo: str) -> Desapropriacao | None:
        pass

    @abstractmethod
    async def list(self, *, imovel_inscricao: str | None=None, status: StatusDesapropriacao | None=None, ativo: bool | None=None) -> list[Desapropriacao]:
        pass

    @abstractmethod
    async def next_numero_processo(self) -> str:
        pass