from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.public_security.domain.enums import StatusMandado, TipoMandado
from apps.backend.app.modules.public_security.domain.models.mandado import Mandado

class MandadoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, mandado: Mandado) -> Mandado:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, mandado_id: UUID) -> Mandado | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_numero(self, numero_mandado: str) -> Mandado | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[Mandado]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Mandado]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoMandado) -> list[Mandado]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusMandado) -> list[Mandado]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, mandado_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_numero(self) -> str:
        raise NotImplementedError