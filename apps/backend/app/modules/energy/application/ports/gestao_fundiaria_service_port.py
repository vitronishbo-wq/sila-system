from __future__ import annotations

from abc import ABC, abstractmethod


class GestaoFundiariaServicePort(ABC):
    @abstractmethod
    async def validar_area_implantacao(self, municipio: str, provincia: str) -> bool:
        pass
