from ...application.ports.documento_provider_port import DocumentoProviderPort
from ...domain.exceptions import (
    TipoDocumentoNaoSuportadoError,
)
from ...domain.models import (
    DocumentVerificationResult,
    DocumentoStatus,
    DocumentoVerificavel,
    MetodoVerificacao,
    TipoDocumento,
)


class VerificacaoDocumentalService:
    TIPOS_SUPORTADOS = {
        TipoDocumento.BI,
        TipoDocumento.PASSPORT,
        TipoDocumento.CERTIFICADO_NASCIMENTO,
        TipoDocumento.CERTIFICADO_CONCLUSAO,
        TipoDocumento.DIPLOMA,
        TipoDocumento.FOTOGRAFIA,
        TipoDocumento.COMPROVANTE_MORADA,
    }

    def __init__(self, provider: DocumentoProviderPort | None = None):
        self._provider = provider

    def _validar_tipo(self, tipo: TipoDocumento) -> None:
        if tipo not in self.TIPOS_SUPORTADOS:
            raise TipoDocumentoNaoSuportadoError(tipo.value)

    def _verificar_tamanho(self, documento: DocumentoVerificavel) -> list[str]:
        problemas = []
        if documento.base64_content and len(documento.base64_content) > 10 * 1024 * 1024:
            problemas.append("Documento excede 10MB")
        return problemas

    async def verificar(self, tipo: TipoDocumento, base64_content: str) -> DocumentVerificationResult:
        self._validar_tipo(tipo)
        documento = DocumentoVerificavel(tipo=tipo, base64_content=base64_content)
        problemas = self._verificar_tamanho(documento)
        if problemas:
            return DocumentVerificationResult(
                documento_tipo=tipo,
                valido=False,
                status=DocumentoStatus.REPROVADO,
                metodo=MetodoVerificacao.MANUAL,
                problemas=problemas,
                confianca_global=0.0,
            )
        if self._provider:
            return await self._provider.verificar(documento)
        return DocumentVerificationResult(
            documento_tipo=tipo,
            valido=True,
            status=DocumentoStatus.PENDENTE,
            metodo=MetodoVerificacao.OCR,
            confianca_global=0.5,
        )

    async def extrair_campos(self, tipo: TipoDocumento, base64_content: str) -> dict[str, str]:
        self._validar_tipo(tipo)
        documento = DocumentoVerificavel(tipo=tipo, base64_content=base64_content)
        if self._provider:
            return await self._provider.extrair_campos(documento)
        return {}
