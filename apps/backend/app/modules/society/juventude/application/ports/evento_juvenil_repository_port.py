from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.enums import StatusEvento
from apps.backend.app.modules.society.juventude.domain.models.evento_juvenil import EventoJuvenil


class EventoJuvenilRepositoryPort(ABC):
    @abstractmethod
    async def save(self, evento: EventoJuvenil) -> EventoJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, evento_id: UUID) -> EventoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_evento: str) -> EventoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[EventoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusEvento) -> list[EventoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, evento_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
