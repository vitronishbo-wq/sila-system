import re

from ...domain.exceptions import (
    NifNaoEncontradoError,
    NifNumeroInvalidoError,
)
from ...domain.models import (
    NifData,
    NifStatus,
    NifVerificationResult,
)
from ...application.ports.nif_provider_port import (
    NifProviderPort,
)


class NifService:
    def __init__(self, provider: NifProviderPort):
        self._provider = provider

    def _validar_formato(self, nif: str) -> bool:
        if not nif:
            return False
        return bool(re.match(r"^\d{10}$", nif))

    def _calcular_digito_controle(self, nif: str) -> bool:
        if len(nif) != 10:
            return False
        total = sum(int(d) * (10 - i) for i, d in enumerate(nif[:9]))
        resto = total % 11
        digito_esperado = 0 if resto < 2 else 11 - resto
        return digito_esperado == int(nif[9])

    async def validar(self, nif: str) -> NifVerificationResult:
        if not self._validar_formato(nif):
            raise NifNumeroInvalidoError(nif)
        return await self._provider.validar_nif(nif)

    async def consultar(self, nif: str) -> NifData:
        if not self._validar_formato(nif):
            raise NifNumeroInvalidoError(nif)
        dados = await self._provider.consultar_nif(nif)
        if dados is None:
            raise NifNaoEncontradoError(nif)
        return dados

    async def verificar_validade(self, nif: str) -> bool:
        status = await self._provider.verificar_status(nif)
        return status == NifStatus.ATIVO
