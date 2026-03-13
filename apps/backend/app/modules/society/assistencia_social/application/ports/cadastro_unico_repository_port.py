from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.assistencia_social.domain.models import CadastroUnico

class CadastroUnicoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, entity: CadastroUnico) -> CadastroUnico:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> CadastroUnico | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> CadastroUnico | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[CadastroUnico]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError