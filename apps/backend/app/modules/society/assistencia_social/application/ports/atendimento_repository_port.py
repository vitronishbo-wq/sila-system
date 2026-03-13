from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.assistencia_social.domain.models import Atendimento

class AtendimentoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, entity: Atendimento) -> Atendimento:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Atendimento | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_beneficiario(self, beneficiario_id: UUID) -> list[Atendimento]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Atendimento]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        raise NotImplementedError