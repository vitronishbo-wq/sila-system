from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

class ComercioExternoServicePort(ABC):

    @abstractmethod
    async def registrar_exportacao_pescado(self, *, captura_id: UUID, destino: str, quantidade_kg: Decimal) -> bool:
        pass