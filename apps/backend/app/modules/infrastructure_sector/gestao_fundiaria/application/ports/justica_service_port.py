from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID

class JusticaServicePort(ABC):

    @abstractmethod
    async def possui_litigio_ativo(self, imovel_id: UUID) -> bool:
        pass

    @abstractmethod
    async def validar_matricula(self, numero_matricula: str, cartorio_nome: str, livro: str, folha: str) -> bool:
        pass