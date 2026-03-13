class MediacaoService:

    async def iniciar_mediacao(self, reclamacao_id: int) -> dict:
        return {'reclamacao_id': reclamacao_id, 'status': 'agendada'}