from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma
from app.modules.society.juventude.domain.models.programa_juvenil import ProgramaJuvenil

class ProgramaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, programa: ProgramaJuvenil) -> ProgramaJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, programa_id: UUID) -> ProgramaJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_programa: str) -> ProgramaJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[ProgramaJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_tipo(self, tipo: TipoPrograma) -> list[ProgramaJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusPrograma) -> list[ProgramaJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, programa_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError