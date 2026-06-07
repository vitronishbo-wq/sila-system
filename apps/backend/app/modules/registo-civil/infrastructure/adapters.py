class RegistoCivilXRoadMockAdapter:
    async def notificar_obito(self, bi_numero: str, data_obito: str) -> dict:
        return {"status": "notificado", "bi": bi_numero}

    async def verificar_bi_falecido(self, bi_numero: str) -> bool:
        return False

    async def sincronizar_nascimento(self, registo_id: str) -> dict:
        return {"status": "sincronizado", "id": registo_id}
