from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.assistencia_social.domain.models import ProgramaSocial

class ProgramaSocialRepositoryPort(ABC):

    @abstractmethod
    async def save(self, entity: ProgramaSocial) -> ProgramaSocial:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> ProgramaSocial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> ProgramaSocial | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[ProgramaSocial]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError