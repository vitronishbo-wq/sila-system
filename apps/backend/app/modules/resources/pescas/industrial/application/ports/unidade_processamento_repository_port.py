from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.pescas.industrial.domain.enums import TipoProcessamento
from app.modules.resources.pescas.industrial.domain.models.unidade_processamento import UnidadeProcessamento

class UnidadeProcessamentoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, unidade: UnidadeProcessamento) -> UnidadeProcessamento:
        pass

    @abstractmethod
    async def get_by_id(self, unidade_id: UUID) -> UnidadeProcessamento | None:
        pass

    @abstractmethod
    async def get_by_cnpj(self, cnpj: str) -> UnidadeProcessamento | None:
        pass

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[UnidadeProcessamento]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoProcessamento) -> list[UnidadeProcessamento]:
        pass

    @abstractmethod
    async def list_all(self) -> list[UnidadeProcessamento]:
        pass

    @abstractmethod
    async def delete(self, unidade_id: UUID) -> bool:
        pass