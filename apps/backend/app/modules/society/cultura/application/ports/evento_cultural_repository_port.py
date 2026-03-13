from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID
from apps.backend.app.modules.society.cultura.domain.enums import StatusEventoCultural, TipoEventoCultural
from apps.backend.app.modules.society.cultura.domain.models.evento_cultural import EventoCultural

class EventoCulturalRepositoryPort(ABC):

    @abstractmethod
    async def save(self, evento: EventoCultural) -> EventoCultural:
        pass

    @abstractmethod
    async def get_by_id(self, evento_id: UUID) -> EventoCultural | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_evento: str) -> EventoCultural | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[EventoCultural]:
        pass

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoEventoCultural) -> list[EventoCultural]:
        pass

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[EventoCultural]:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusEventoCultural) -> list[EventoCultural]:
        pass

    @abstractmethod
    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[EventoCultural]:
        pass

    @abstractmethod
    async def delete(self, evento_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass