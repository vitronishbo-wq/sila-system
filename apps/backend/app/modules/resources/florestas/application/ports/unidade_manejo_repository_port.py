from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.florestas.domain.enums import TipoManejo
from app.modules.resources.florestas.domain.models.unidade_manejo import UnidadeManejo

class UnidadeManejoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, unidade: UnidadeManejo) -> UnidadeManejo:
        pass

    @abstractmethod
    async def get_by_id(self, unidade_id: UUID) -> UnidadeManejo | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_um: str) -> UnidadeManejo | None:
        pass

    @abstractmethod
    async def list_by_operador(self, operador_id: UUID) -> list[UnidadeManejo]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo_manejo: TipoManejo) -> list[UnidadeManejo]:
        pass

    @abstractmethod
    async def next_codigo(self, operador_id: UUID) -> str:
        pass