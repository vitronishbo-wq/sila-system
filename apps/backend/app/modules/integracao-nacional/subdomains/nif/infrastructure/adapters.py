from ..application.ports.nif_provider_port import NifProviderPort
from ..domain.models import (
    NifData,
    NifStatus,
    NifTipoContribuinte,
    NifVerificationResult,
)


class NifAGTMockAdapter(NifProviderPort):
    async def validar_nif(self, nif: str) -> NifVerificationResult:
        return NifVerificationResult(
            nif=nif,
            valido=True,
            status=NifStatus.ATIVO,
            contribuinte_encontrado=True,
            fonte="agt",
        )

    async def consultar_nif(self, nif: str) -> NifData | None:
        return NifData(nif=nif, full_name="CONSULTA_AGT", tipo=NifTipoContribuinte.SINGULAR, status=NifStatus.ATIVO)

    async def verificar_status(self, nif: str) -> NifStatus:
        return NifStatus.ATIVO


class NifMockAdapter(NifProviderPort):
    def __init__(self):
        self._database: dict[str, NifData] = {}

    def seed(self, data: NifData):
        self._database[data.nif] = data

    async def validar_nif(self, nif: str) -> NifVerificationResult:
        encontrado = nif in self._database
        dados = self._database.get(nif)
        return NifVerificationResult(
            nif=nif,
            valido=encontrado and dados.status == NifStatus.ATIVO,
            status=dados.status if dados else NifStatus.NAO_ENCONTRADO,
            contribuinte_encontrado=encontrado,
            dados=dados,
            fonte="mock",
        )

    async def consultar_nif(self, nif: str) -> NifData | None:
        return self._database.get(nif)

    async def verificar_status(self, nif: str) -> NifStatus:
        dados = self._database.get(nif)
        if not dados:
            return NifStatus.NAO_ENCONTRADO
        return dados.status
