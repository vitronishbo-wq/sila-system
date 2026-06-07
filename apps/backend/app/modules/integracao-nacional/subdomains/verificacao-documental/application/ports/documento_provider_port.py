from abc import ABC, abstractmethod

from ...domain.models import (
    DocumentVerificationResult,
    DocumentoVerificavel,
)


class DocumentoProviderPort(ABC):
    @abstractmethod
    async def verificar(self, documento: DocumentoVerificavel) -> DocumentVerificationResult:
        pass

    @abstractmethod
    async def extrair_campos(self, documento: DocumentoVerificavel) -> dict[str, str]:
        pass

    @abstractmethod
    async def validar_assinatura(self, documento: DocumentoVerificavel, assinatura: str) -> bool:
        pass
