from ..application.ports.documento_provider_port import DocumentoProviderPort
from ..domain.models import (
    CampoExtraido,
    DocumentVerificationResult,
    DocumentoStatus,
    DocumentoVerificavel,
    MetodoVerificacao,
)


class DocumentoOCRAnalyser(DocumentoProviderPort):
    async def verificar(self, documento: DocumentoVerificavel) -> DocumentVerificationResult:
        confianca = 0.6 if documento.base64_content else 0.0
        return DocumentVerificationResult(
            documento_tipo=documento.tipo,
            valido=confianca > 0.5,
            status=DocumentoStatus.VERIFICADO if confianca > 0.5 else DocumentoStatus.INCONCLUSIVO,
            metodo=MetodoVerificacao.OCR,
            confianca_global=confianca,
        )

    async def extrair_campos(self, documento: DocumentoVerificavel) -> dict[str, str]:
        return {"tipo": documento.tipo.value, "status": "extraido"}

    async def validar_assinatura(self, documento: DocumentoVerificavel, assinatura: str) -> bool:
        return bool(assinatura)


class DocumentoMockAdapter(DocumentoProviderPort):
    async def verificar(self, documento: DocumentoVerificavel) -> DocumentVerificationResult:
        return DocumentVerificationResult(
            documento_tipo=documento.tipo,
            valido=True,
            status=DocumentoStatus.VERIFICADO,
            metodo=MetodoVerificacao.MANUAL,
            campos_extraidos=[CampoExtraido(nome="nome", valor="MOCK", confianca=1.0)],
            confianca_global=1.0,
        )

    async def extrair_campos(self, documento: DocumentoVerificavel) -> dict[str, str]:
        return {"nome": "MOCK", "tipo": documento.tipo.value}

    async def validar_assinatura(self, documento: DocumentoVerificavel, assinatura: str) -> bool:
        return True
