from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.intelligence.ciencia_pesquisa.domain.models.instituicao_pesquisa import InstituicaoPesquisa

class InstituicaoPesquisaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, instituicao: InstituicaoPesquisa) -> InstituicaoPesquisa:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, instituicao_id: UUID) -> InstituicaoPesquisa | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_sigla(self, sigla: str) -> InstituicaoPesquisa | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_nif(self, nif: str) -> InstituicaoPesquisa | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[InstituicaoPesquisa]:
        raise NotImplementedError

    @abstractmethod
    async def list_ativas(self) -> list[InstituicaoPesquisa]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instituicao_id: UUID) -> bool:
        raise NotImplementedError