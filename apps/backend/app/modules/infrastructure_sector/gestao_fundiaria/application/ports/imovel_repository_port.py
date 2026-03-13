from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.infrastructure_sector.gestao_fundiaria.domain.models.imovel import Imovel

class ImovelRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Imovel) -> Imovel:
        pass

    @abstractmethod
    async def get_by_inscricao(self, inscricao_imobiliaria: str) -> Imovel | None:
        pass

    @abstractmethod
    async def list(self, *, proprietario_atual_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None, ativo: bool | None=None) -> list[Imovel]:
        pass

    @abstractmethod
    async def next_inscricao(self) -> str:
        pass