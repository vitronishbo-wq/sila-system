from __future__ import annotations
from abc import ABC, abstractmethod

class ComercioServicosServicePort(ABC):

    @abstractmethod
    async def list_parceiros_turisticos(self, *, municipio: str) -> list[str]:
        pass

    @abstractmethod
    async def agencia_cnpj_ativo(self, *, cnpj: str) -> bool:
        pass