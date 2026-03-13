from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.juventude.domain.enums import StatusVoluntariado
from apps.backend.app.modules.society.juventude.domain.models.voluntariado import Voluntariado

class VoluntariadoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, voluntariado: Voluntariado) -> Voluntariado:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, voluntariado_id: UUID) -> Voluntariado | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_voluntariado: str) -> Voluntariado | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Voluntariado]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[Voluntariado]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusVoluntariado) -> list[Voluntariado]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, voluntariado_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError