import re

from ...domain.exceptions import (
    BiNaoEncontradoError,
    BiNumeroInvalidoError,
)
from ...domain.models import (
    BilheteIdentidade,
    BiStatus,
    BiVerificationResult,
)
from ...application.ports.bi_provider_port import BiProviderPort


class BiService:
    def __init__(self, provider: BiProviderPort):
        self._provider = provider

    def _validar_formato(self, bi_numero: str) -> bool:
        if not bi_numero or len(bi_numero) < 6:
            return False
        return bool(re.match(r"^[A-Z0-9]{6,14}$", bi_numero.upper()))

    async def validar(self, bi_numero: str) -> BiVerificationResult:
        if not self._validar_formato(bi_numero):
            raise BiNumeroInvalidoError(bi_numero)
        return await self._provider.validar_bi(bi_numero)

    async def consultar(self, bi_numero: str) -> BilheteIdentidade:
        if not self._validar_formato(bi_numero):
            raise BiNumeroInvalidoError(bi_numero)
        dados = await self._provider.consultar_bi(bi_numero)
        if dados is None:
            raise BiNaoEncontradoError(bi_numero)
        return dados

    async def verificar_biometria(self, bi_numero: str, fingerprint_hash: str) -> bool:
        if not self._validar_formato(bi_numero):
            raise BiNumeroInvalidoError(bi_numero)
        return await self._provider.verificar_biometria(bi_numero, fingerprint_hash)

    async def verificar_validade(self, bi_numero: str) -> bool:
        status = await self._provider.verificar_status(bi_numero)
        return status == BiStatus.VALIDO
