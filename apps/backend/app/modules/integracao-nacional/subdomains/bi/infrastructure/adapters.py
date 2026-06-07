from ..application.ports.bi_provider_port import BiProviderPort
from ..domain.models import (
    BilheteIdentidade,
    BiStatus,
    BiTipo,
    BiVerificationResult,
)


class BiXRoadMockAdapter(BiProviderPort):
    def __init__(self, xroad_client=None):
        self._xroad = xroad_client

    async def validar_bi(self, bi_numero: str) -> BiVerificationResult:
        return BiVerificationResult(
            bi_numero=bi_numero,
            valido=True,
            status=BiStatus.VALIDO,
            cidadao_encontrado=True,
            fonte="xroad",
        )

    async def consultar_bi(self, bi_numero: str) -> BilheteIdentidade | None:
        return BilheteIdentidade(
            numero=bi_numero,
            full_name="CONSULTA_XROAD",
            birth_date="1900-01-01",
            gender="M",
            tipo=BiTipo.NORMAL,
            status=BiStatus.VALIDO,
        )

    async def verificar_biometria(self, bi_numero: str, fingerprint_hash: str) -> bool:
        return True

    async def verificar_status(self, bi_numero: str) -> BiStatus:
        return BiStatus.VALIDO


class BiMockAdapter(BiProviderPort):
    def __init__(self):
        self._database: dict[str, BilheteIdentidade] = {}

    def seed(self, bi: BilheteIdentidade):
        self._database[bi.numero] = bi

    async def validar_bi(self, bi_numero: str) -> BiVerificationResult:
        encontrado = bi_numero in self._database
        dados = self._database.get(bi_numero)
        return BiVerificationResult(
            bi_numero=bi_numero,
            valido=encontrado and dados.status == BiStatus.VALIDO,
            status=dados.status if dados else BiStatus.NAO_ENCONTRADO,
            cidadao_encontrado=encontrado,
            dados=dados,
            fonte="mock",
        )

    async def consultar_bi(self, bi_numero: str) -> BilheteIdentidade | None:
        return self._database.get(bi_numero)

    async def verificar_biometria(self, bi_numero: str, fingerprint_hash: str) -> bool:
        bi = self._database.get(bi_numero)
        if not bi:
            return False
        return bi.fingerprint_hash == fingerprint_hash

    async def verificar_status(self, bi_numero: str) -> BiStatus:
        bi = self._database.get(bi_numero)
        if not bi:
            return BiStatus.NAO_ENCONTRADO
        return bi.status
