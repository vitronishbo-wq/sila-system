from __future__ import annotations

from abc import ABC, abstractmethod


class ComercioExternoServicePort(ABC):
    @abstractmethod
    async def validar_corredor_exportacao(self, codigo: str) -> bool:
        pass
