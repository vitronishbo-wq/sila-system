from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.civil_protection.domain.enums import StatusAtendimento
from apps.backend.app.modules.civil_protection.domain.models.atendimento import Atendimento

class AtendimentoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, atendimento: Atendimento) -> Atendimento:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, atendimento_id: UUID) -> Atendimento | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_atendimento: str) -> Atendimento | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Atendimento]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Atendimento]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_despacho(self, despacho_id: UUID) -> list[Atendimento]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusAtendimento) -> list[Atendimento]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, atendimento_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError