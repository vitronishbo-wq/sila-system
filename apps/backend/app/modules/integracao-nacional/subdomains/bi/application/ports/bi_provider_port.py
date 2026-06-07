from abc import ABC, abstractmethod

from ...domain.models import (
    BilheteIdentidade,
    BiStatus,
    BiVerificationResult,
)


class BiProviderPort(ABC):
    @abstractmethod
    async def validar_bi(self, bi_numero: str) -> BiVerificationResult:
        pass

    @abstractmethod
    async def consultar_bi(self, bi_numero: str) -> BilheteIdentidade | None:
        pass

    @abstractmethod
    async def verificar_biometria(self, bi_numero: str, fingerprint_hash: str) -> bool:
        pass

    @abstractmethod
    async def verificar_status(self, bi_numero: str) -> BiStatus:
        pass
