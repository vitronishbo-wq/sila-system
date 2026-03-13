from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class EmpregoAdapterPort(ABC):

    @abstractmethod
    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_status_candidato(self, citizen_id: UUID) -> str | None:
        raise NotImplementedError