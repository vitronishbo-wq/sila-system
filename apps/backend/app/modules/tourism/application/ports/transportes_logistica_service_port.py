from __future__ import annotations
from abc import ABC, abstractmethod

class TransportesLogisticaServicePort(ABC):

    @abstractmethod
    async def list_opcoes_transporte(self, *, origem: str, destino: str) -> list[str]:
        pass

    @abstractmethod
    async def estimate_tempo_viagem_horas(self, *, origem: str, destino: str, modal: str | None=None) -> float | None:
        pass