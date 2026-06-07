from __future__ import annotations

from abc import ABC, abstractmethod


class SegurancaPublicaServicePort(ABC):
    @abstractmethod
    async def validar_regularidade_veiculo(self, *, placa: str) -> bool:
        pass
