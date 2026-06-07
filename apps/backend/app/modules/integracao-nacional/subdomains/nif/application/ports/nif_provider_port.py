from abc import ABC, abstractmethod

from ...domain.models import (
    NifData,
    NifStatus,
    NifVerificationResult,
)


class NifProviderPort(ABC):
    @abstractmethod
    async def validar_nif(self, nif: str) -> NifVerificationResult:
        pass

    @abstractmethod
    async def consultar_nif(self, nif: str) -> NifData | None:
        pass

    @abstractmethod
    async def verificar_status(self, nif: str) -> NifStatus:
        pass
