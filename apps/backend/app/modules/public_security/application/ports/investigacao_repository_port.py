from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.public_security.domain.enums import StatusInvestigacao
from apps.backend.app.modules.public_security.domain.models.investigacao import Investigacao

class InvestigacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, investigacao: Investigacao) -> Investigacao:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, investigacao_id: UUID) -> Investigacao | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_investigacao: str) -> Investigacao | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Investigacao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Investigacao]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusInvestigacao) -> list[Investigacao]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, investigacao_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError