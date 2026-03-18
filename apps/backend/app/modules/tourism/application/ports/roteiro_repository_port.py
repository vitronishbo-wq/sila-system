from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.tourism.domain.models.roteiro import Roteiro

class RoteiroRepositoryPort(ABC):

    @abstractmethod
    async def save(self, roteiro: Roteiro) -> Roteiro:
        pass

    @abstractmethod
    async def get_by_id(self, roteiro_id: UUID) -> Roteiro | None:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo: str) -> Roteiro | None:
        pass

    @abstractmethod
    async def list(self, *, municipio_origem: str | None=None, ativo: bool | None=None) -> list[Roteiro]:
        pass

    @abstractmethod
    async def delete(self, roteiro_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_codigo(self, provincia: str) -> str:
        pass