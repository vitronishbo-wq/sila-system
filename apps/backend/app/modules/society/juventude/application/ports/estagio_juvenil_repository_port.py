from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.juventude.domain.enums import StatusEstagio
from app.modules.society.juventude.domain.models.estagio_juvenil import EstagioJuvenil

class EstagioJuvenilRepositoryPort(ABC):

    @abstractmethod
    async def save(self, estagio: EstagioJuvenil) -> EstagioJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, estagio_id: UUID) -> EstagioJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_estagio: str) -> EstagioJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[EstagioJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[EstagioJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusEstagio) -> list[EstagioJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, estagio_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError