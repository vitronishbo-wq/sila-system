from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.intelligence.ciencia_pesquisa.domain.models.pesquisador import Pesquisador

class PesquisadorRepositoryPort(ABC):

    @abstractmethod
    async def save(self, pesquisador: Pesquisador) -> Pesquisador:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, pesquisador_id: UUID) -> Pesquisador | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_documento(self, documento_identificacao: str) -> Pesquisador | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email_institucional: str) -> Pesquisador | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Pesquisador]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_instituicao(self, instituicao_id: UUID) -> list[Pesquisador]:
        raise NotImplementedError

    @abstractmethod
    async def vincular_instituicao(self, *, pesquisador_id: UUID, instituicao_id: UUID, unidade_pesquisa_id: UUID | None=None) -> Pesquisador | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pesquisador_id: UUID) -> bool:
        raise NotImplementedError