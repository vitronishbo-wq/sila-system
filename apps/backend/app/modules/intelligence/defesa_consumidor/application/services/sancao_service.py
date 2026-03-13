class SancaoService:

    async def aplicar_sancao(self, reclamacao_id: int, tipo: str) -> dict:
        return {'reclamacao_id': reclamacao_id, 'tipo': tipo, 'status': 'aplicada'}