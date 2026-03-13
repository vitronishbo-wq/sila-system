from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class AmbienteServicePort(ABC):

    @abstractmethod
    async def validar_licenca_ambiental(self, obra_id: UUID) -> bool:
        pass