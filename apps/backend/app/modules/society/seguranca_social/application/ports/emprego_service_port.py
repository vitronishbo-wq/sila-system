from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class EmpregoServicePort(ABC):
    @abstractmethod
    async def is_candidato_registrado(self, citizen_id: UUID) -> bool:
        pass
