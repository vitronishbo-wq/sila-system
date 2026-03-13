from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoOutorga
from app.modules.resources.aguas_saneamento.domain.models.outorga import Outorga

class OutorgaRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Outorga) -> Outorga:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_outorga: str) -> Outorga | None:
        pass

    @abstractmethod
    async def list(self, *, requerente_id: UUID | None=None, tipo: TipoOutorga | None=None, status: StatusOutorga | None=None) -> list[Outorga]:
        pass

    @abstractmethod
    async def next_numero(self) -> str:
        pass