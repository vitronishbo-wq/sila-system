from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.app.modules.civil_protection.domain.enums import StatusDespacho
from apps.backend.app.modules.civil_protection.domain.models.despacho import Despacho


class DespachoRepositoryPort(ABC):
    @abstractmethod
    async def save(self, despacho: Despacho) -> Despacho:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, despacho_id: UUID) -> Despacho | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_despacho: str) -> Despacho | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Despacho]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Despacho]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusDespacho) -> list[Despacho]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, despacho_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError
