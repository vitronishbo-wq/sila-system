from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.governance.statistics.domain.enums import FonteDados, TipoMetrica
from app.modules.governance.statistics.domain.models.metrica import Metrica

class MetricaRepositoryPort(ABC):

    @abstractmethod
    async def create(self, metrica: Metrica) -> Metrica:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, metrica_id: int) -> Metrica | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_nome(self, nome: str) -> Metrica | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, limit: int=100, offset: int=0) -> list[Metrica]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_fonte(self, fonte: FonteDados, limit: int=100) -> list[Metrica]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoMetrica, limit: int=100) -> list[Metrica]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, metrica: Metrica) -> Metrica:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, metrica_id: int) -> bool:
        raise NotImplementedError