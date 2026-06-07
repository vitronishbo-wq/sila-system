class MoradaRepository:
    def __init__(self, session=None):
        self._session = session

    async def salvar_normalizacao(self, morada: "MoradaNormalizada") -> None:
        pass

    async def listar_historico(self, limit: int = 50) -> list["MoradaNormalizada"]:
        return []
