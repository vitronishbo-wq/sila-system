class VerificacaoRepository:
    def __init__(self, session=None):
        self._session = session

    async def registrar(self, resultado: "DocumentVerificationResult") -> None:
        pass

    async def listar_verificacoes(self, limit: int = 50) -> list["DocumentVerificationResult"]:
        return []
