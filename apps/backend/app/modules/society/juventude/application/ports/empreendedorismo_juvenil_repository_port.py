from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.juventude.domain.enums import StatusEmpreendimento
from apps.backend.app.modules.society.juventude.domain.models.empreendedorismo_juvenil import EmpreendedorismoJuvenil

class EmpreendedorismoJuvenilRepositoryPort(ABC):

    @abstractmethod
    async def save(self, empreendimento: EmpreendedorismoJuvenil) -> EmpreendedorismoJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, empreendimento_id: UUID) -> EmpreendedorismoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_empreendimento: str) -> EmpreendedorismoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[EmpreendedorismoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[EmpreendedorismoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusEmpreendimento) -> list[EmpreendedorismoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, empreendimento_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError