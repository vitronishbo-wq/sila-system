from __future__ import annotations
from abc import ABC, abstractmethod

class AmbienteServicePort(ABC):

    @abstractmethod
    async def validar_restricao_ambiental(self, origem: str, destino: str) -> bool:
        pass