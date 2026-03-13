from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.public_security.domain.enums import StatusProva, TipoProva
from apps.backend.app.modules.public_security.domain.models.prova_pericial import ProvaPericial

class ProvaPericialRepositoryPort(ABC):

    @abstractmethod
    async def save(self, prova: ProvaPericial) -> ProvaPericial:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, prova_id: UUID) -> ProvaPericial | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_prova: str) -> ProvaPericial | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[ProvaPericial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[ProvaPericial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoProva) -> list[ProvaPericial]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusProva) -> list[ProvaPericial]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, prova_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError