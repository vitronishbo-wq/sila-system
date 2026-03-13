from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusPoliticaJuventude
from apps.backend.app.modules.society.juventude.domain.models.politica_juventude import PoliticaJuventude

class PoliticaJuventudeRepositoryPort(ABC):

    @abstractmethod
    async def save(self, politica: PoliticaJuventude) -> PoliticaJuventude:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, politica_id: UUID) -> PoliticaJuventude | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_politica: str) -> PoliticaJuventude | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[PoliticaJuventude]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusPoliticaJuventude) -> list[PoliticaJuventude]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_area(self, area: AreaInteresse) -> list[PoliticaJuventude]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, politica_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError