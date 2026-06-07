from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class AssistenciaSocialAdapterPort(ABC):
    @abstractmethod
    async def is_beneficiario_ativo(self, citizen_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def has_visita_recente(self, citizen_id: UUID, days: int = 90) -> bool:
        raise NotImplementedError
