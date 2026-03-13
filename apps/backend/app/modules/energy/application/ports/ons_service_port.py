from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.energy.domain.enums import BandeiraTarifaria

class ONSServicePort(ABC):

    @abstractmethod
    async def get_bandeira_tarifaria(self) -> BandeiraTarifaria:
        pass
