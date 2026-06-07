from ..domain.models import BiVerificationResult


class BiVerificationLogRepository:
    def __init__(self, session=None):
        self._session = session

    async def registrar_verificacao(self, result: BiVerificationResult) -> None:
        pass

    async def listar_verificacoes(self, limit: int = 50) -> list[BiVerificationResult]:
        return []

    async def verificar_duplicados(self, bi_numero: str) -> int:
        return 0
