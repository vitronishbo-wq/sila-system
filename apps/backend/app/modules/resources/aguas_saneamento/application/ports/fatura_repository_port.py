from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusFatura
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.fatura_agua import FaturaAgua

class FaturaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: FaturaAgua) -> FaturaAgua:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_fatura: str) -> FaturaAgua | None:
        pass

    @abstractmethod
    async def list(self, *, consumo_id: UUID | None=None, titular_id: UUID | None=None, referencia: str | None=None, status: StatusFatura | None=None) -> list[FaturaAgua]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass