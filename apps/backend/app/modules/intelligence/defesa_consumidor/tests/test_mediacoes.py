import pytest
from apps.backend.app.modules.intelligence.defesa_consumidor.application.services.mediacao_service import MediacaoService

@pytest.mark.asyncio
async def test_iniciar_mediacao():
    service = MediacaoService()
    result = await service.iniciar_mediacao(10)
    assert result['reclamacao_id'] == 10
    assert result['status'] == 'agendada'