from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from app.modules.justice.bounded_contexts.infrastructure.adapters.juventude_service_adapter import JuventudeServiceAdapter
from app.modules.society.juventude.domain.enums import Escolaridade, FaixaEtaria, SituacaoOcupacional, TipoVulnerabilidade

@pytest.mark.asyncio
async def test_adapter_juventude_retorna_perfil_e_risco() -> None:
    citizen_id = uuid4()
    jovem = SimpleNamespace(id=uuid4(), numero_registro='JOV/2026/00001', nome='Maria', faixa_etaria=FaixaEtaria.JOVEM_18_24, escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, vulnerabilidades=[TipoVulnerabilidade.VIOLENCIA_DOMESTICA], ativo=True)
    repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=jovem))
    adapter = JuventudeServiceAdapter(repo)
    perfil = await adapter.get_perfil_jovem(citizen_id)
    em_risco = await adapter.is_jovem_em_risco(citizen_id)
    assert perfil is not None
    assert perfil['numero_registro'] == 'JOV/2026/00001'
    assert perfil['vulnerabilidades'] == [TipoVulnerabilidade.VIOLENCIA_DOMESTICA.value]
    assert em_risco is True