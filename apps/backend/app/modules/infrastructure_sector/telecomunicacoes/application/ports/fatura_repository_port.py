from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.fatura_telecom import FaturaTelecom

class FaturaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, fatura: FaturaTelecom) -> FaturaTelecom:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, fatura_id: UUID) -> FaturaTelecom | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_numero(self, numero_fatura: str) -> FaturaTelecom | None:
        raise NotImplementedError

    @abstractmethod
    async def list_by_assinante(self, assinante_id: UUID) -> list[FaturaTelecom]:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[FaturaTelecom]:
        raise NotImplementedError

    @abstractmethod
    async def next_numero(self) -> str:
        raise NotImplementedError