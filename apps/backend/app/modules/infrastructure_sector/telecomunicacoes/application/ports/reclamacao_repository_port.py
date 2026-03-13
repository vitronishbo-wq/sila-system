from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.reclamacao import Reclamacao

class ReclamacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, reclamacao: Reclamacao) -> Reclamacao:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, reclamacao_id: UUID) -> Reclamacao | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_protocolo(self, protocolo: str) -> Reclamacao | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_assinante(self, assinante_id: UUID) -> list[Reclamacao]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Reclamacao]:
        raise NotImplementedError

    @abstractmethod
    async def next_protocolo(self) -> str:
        raise NotImplementedError