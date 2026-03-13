from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class AguasSaneamentoServicePort(ABC):

    @abstractmethod
    async def validar_capacidade_atendimento(self, *, zoneamento_id: UUID, quantidade_lotes: int) -> bool:
        pass