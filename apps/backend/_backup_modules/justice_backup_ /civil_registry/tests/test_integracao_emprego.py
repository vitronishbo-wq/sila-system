from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from app.modules.society.emprego.domain.enums import Escolaridade, SituacaoProfissional, StatusCandidato
from app.modules.justice.bounded_contexts.infrastructure.adapters.emprego_service_adapter import EmpregoServiceAdapter

@pytest.mark.asyncio
async def test_adapter_emprego_retorna_candidatura_ativa() -> None:
    citizen_id = uuid4()
    candidato = SimpleNamespace(id=uuid4(), numero_processo='CAND/2026/0001', status=StatusCandidato.ATIVO, situacao=SituacaoProfissional.DESEMPREGADO, escolaridade=Escolaridade.SECUNDARIA, areas_interesse=['tecnologia'], observacoes='perfil atualizado')
    repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=candidato))
    adapter = EmpregoServiceAdapter(repo)
    candidatura = await adapter.get_candidatura(citizen_id)
    ativa = await adapter.has_candidatura_ativa(citizen_id)
    assert candidatura is not None
    assert candidatura['numero_processo'] == 'CAND/2026/0001'
    assert candidatura['status'] == StatusCandidato.ATIVO.value
    assert ativa is True