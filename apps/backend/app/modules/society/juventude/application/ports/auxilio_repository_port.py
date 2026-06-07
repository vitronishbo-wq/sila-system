from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.society.juventude.domain.enums import StatusBeneficio, TipoAuxilio
from apps.backend.app.modules.society.juventude.domain.models.auxilio import Auxilio


class AuxilioRepositoryPort(ABC):
    @abstractmethod
    async def save(self, auxilio: Auxilio) -> Auxilio:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, auxilio_id: UUID) -> Auxilio | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_auxilio: str) -> Auxilio | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Auxilio]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[Auxilio]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoAuxilio) -> list[Auxilio]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusBeneficio) -> list[Auxilio]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, auxilio_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
