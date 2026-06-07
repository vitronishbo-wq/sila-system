from __future__ import annotations

from abc import ABC, abstractmethod


class TransportesLogisticaServicePort(ABC):
    @abstractmethod
    async def validar_cadeia_frio(self, lote_codigo: str) -> bool:
        pass
