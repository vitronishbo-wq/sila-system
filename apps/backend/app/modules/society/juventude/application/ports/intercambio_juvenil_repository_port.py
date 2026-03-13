from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.juventude.domain.enums import StatusIntercambio
from apps.backend.app.modules.society.juventude.domain.models.intercambio_juvenil import IntercambioJuvenil

class IntercambioJuvenilRepositoryPort(ABC):

    @abstractmethod
    async def save(self, intercambio: IntercambioJuvenil) -> IntercambioJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, intercambio_id: UUID) -> IntercambioJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_intercambio: str) -> IntercambioJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[IntercambioJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[IntercambioJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusIntercambio) -> list[IntercambioJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, intercambio_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError