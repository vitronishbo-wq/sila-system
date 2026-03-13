from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.public_security.domain.enums import StatusEvidencia
from apps.backend.app.modules.public_security.domain.models.evidencia import Evidencia

class EvidenciaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, evidencia: Evidencia) -> Evidencia:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, evidencia_id: UUID) -> Evidencia | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_evidencia: str) -> Evidencia | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Evidencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_vestigio(self, vestigio_id: UUID) -> list[Evidencia]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusEvidencia) -> list[Evidencia]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, evidencia_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError