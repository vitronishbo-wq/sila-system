from __future__ import annotations
from abc import ABC, abstractmethod

class FederacaoServicePort(ABC):

    @abstractmethod
    async def validar_clube_federado(self, codigo_clube: str) -> bool:
        raise NotImplementedError