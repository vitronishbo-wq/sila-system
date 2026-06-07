from __future__ import annotations

from abc import ABC, abstractmethod


class AmbienteServicePort(ABC):
    @abstractmethod
    async def validar_licenca_ambiental(self, licenca_id: str) -> bool:
        pass
