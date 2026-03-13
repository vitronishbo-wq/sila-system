from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.pescas.domain.enums import TipoEmbarcacao
from apps.backend.app.modules.resources.pescas.domain.models.embarcacao import Embarcacao

class EmbarcacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, embarcacao: Embarcacao) -> Embarcacao:
        pass

    @abstractmethod
    async def get_by_id(self, embarcacao_id: UUID) -> Embarcacao | None:
        pass

    @abstractmethod
    async def get_by_inscricao(self, numero_inscricao: str) -> Embarcacao | None:
        pass

    @abstractmethod
    async def list_by_proprietario(self, proprietario_id: UUID) -> list[Embarcacao]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoEmbarcacao) -> list[Embarcacao]:
        pass

    @abstractmethod
    async def next_inscricao(self, porto: str) -> str:
        pass