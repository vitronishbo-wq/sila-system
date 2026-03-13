from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.juventude.domain.enums import StatusInscricao
from app.modules.society.juventude.domain.models.inscricao_programa import InscricaoPrograma

class InscricaoProgramaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, inscricao: InscricaoPrograma) -> InscricaoPrograma:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, inscricao_id: UUID) -> InscricaoPrograma | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_inscricao: str) -> InscricaoPrograma | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[InscricaoPrograma]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[InscricaoPrograma]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_programa(self, programa_id: UUID) -> list[InscricaoPrograma]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusInscricao) -> list[InscricaoPrograma]:
        raise NotImplementedError

    @abstractmethod
    async def exists_active_by_jovem_programa(self, jovem_id: UUID, programa_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def count_confirmadas_by_programa(self, programa_id: UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, inscricao_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError