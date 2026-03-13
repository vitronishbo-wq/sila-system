from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, SituacaoBeneficiario
from app.modules.justice.bounded_contexts.infrastructure.adapters.assistencia_social_service_adapter import AssistenciaSocialServiceAdapter

@pytest.mark.asyncio
async def test_adapter_assistencia_retorna_beneficiario_ativo() -> None:
    citizen_id = uuid4()
    beneficiario = SimpleNamespace(id=uuid4(), numero_registro='BEN/2026/00001', situacao=SituacaoBeneficiario.ATIVO, faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA, ativo=True, cadastro_unico_id=uuid4())
    repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=beneficiario))
    adapter = AssistenciaSocialServiceAdapter(repo)
    item = await adapter.get_beneficiario(citizen_id)
    ativo = await adapter.is_beneficiario_ativo(citizen_id)
    assert item is not None
    assert item['numero_registro'] == 'BEN/2026/00001'
    assert item['situacao'] == SituacaoBeneficiario.ATIVO.value
    assert ativo is True