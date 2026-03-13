from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.assistencia_social.domain.models import Beneficiario

class BeneficiarioRepositoryPort(ABC):

    @abstractmethod
    async def save(self, entity: Beneficiario) -> Beneficiario:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Beneficiario | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> Beneficiario | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Beneficiario]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError