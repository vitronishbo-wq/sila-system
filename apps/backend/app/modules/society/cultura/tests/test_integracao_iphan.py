from __future__ import annotations
import asyncio
from uuid import uuid4
from apps.backend.app.modules.society.cultura.infrastructure.adapters.iphan_adapter import IphanAdapter

def test_iphan_adapter_modo_simulado() -> None:

    async def scenario() -> None:
        adapter = IphanAdapter()
        result = await adapter.registrar_bem_tombado({'bem_id': str(uuid4()), 'nome': 'Fortaleza X', 'tipo': 'historico'})
        assert result['status'] == 'simulado'
        assert 'codigo_iphan' in result
    asyncio.run(scenario())