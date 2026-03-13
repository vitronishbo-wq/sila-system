from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class AmbienteServicePort(ABC):

    @abstractmethod
    async def validar_corpo_hidrico(self, corpo_hidrico_id: UUID) -> bool:
        pass