class NifVerificationLogRepository:
    def __init__(self, session=None):
        self._session = session

    async def registrar_verificacao(self, nif: str, valido: bool) -> None:
        pass

    async def listar_verificacoes(self, limit: int = 50) -> list[dict]:
        return []
