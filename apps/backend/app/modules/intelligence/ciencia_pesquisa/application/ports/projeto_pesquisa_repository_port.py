from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.intelligence.ciencia_pesquisa.domain.models.projeto_pesquisa import ProjetoPesquisa

class ProjetoPesquisaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, projeto: ProjetoPesquisa) -> ProjetoPesquisa:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, projeto_id: UUID) -> ProjetoPesquisa | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoPesquisa | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[ProjetoPesquisa]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_instituicao(self, instituicao_id: UUID) -> list[ProjetoPesquisa]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_pesquisador(self, pesquisador_id: UUID) -> list[ProjetoPesquisa]:
        raise NotImplementedError

    @abstractmethod
    async def vincular_pesquisadores(self, *, projeto_id: UUID, pesquisador_ids: list[UUID]) -> ProjetoPesquisa | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, projeto_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError