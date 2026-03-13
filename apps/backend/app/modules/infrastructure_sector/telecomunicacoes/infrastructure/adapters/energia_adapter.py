from __future__ import annotations

class EnergiaAdapter:
    """Adapter para consumo energetico de torres e estacoes."""

    async def consultar_consumo(self, ativo_id: str) -> dict[str, str]:
        return {'ativo_id': ativo_id, 'status': 'not_configured'}