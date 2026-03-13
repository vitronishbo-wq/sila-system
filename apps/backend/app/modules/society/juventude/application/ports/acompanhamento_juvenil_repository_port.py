from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.society.juventude.domain.enums import StatusAcompanhamento
from app.modules.society.juventude.domain.models.acompanhamento_juvenil import AcompanhamentoJuvenil

class AcompanhamentoJuvenilRepositoryPort(ABC):

    @abstractmethod
    async def save(self, acompanhamento: AcompanhamentoJuvenil) -> AcompanhamentoJuvenil:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, acompanhamento_id: UUID) -> AcompanhamentoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_codigo(self, codigo_acompanhamento: str) -> AcompanhamentoJuvenil | None:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[AcompanhamentoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_jovem(self, jovem_id: UUID) -> list[AcompanhamentoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_status(self, status: StatusAcompanhamento) -> list[AcompanhamentoJuvenil]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, acompanhamento_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def next_codigo(self) -> str:
        raise NotImplementedError