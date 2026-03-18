from __future__ import annotations
import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from apps.backend.app.modules.educacao.application.inscricao_service import InscricaoService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models.inscricao_basica import InscricaoBasica

def test_inscricao_basica_domain_transitions():
    inscricao = InscricaoBasica(id=uuid4(), numero_processo='INS/BASICA/2026/0001', citizen_id=uuid4(), escola_id=uuid4(), data_inscricao=date.today())
    assert inscricao.status == StatusFluxo.PENDENTE
    inscricao.confirmar()
    assert inscricao.status == StatusFluxo.CONFIRMADA

def test_inscricao_service_cria_e_rastreia_request():
    citizen_id = uuid4()
    escola_id = uuid4()
    saved = InscricaoBasica(id=uuid4(), numero_processo='INS/BASICA/2026/0002', citizen_id=citizen_id, escola_id=escola_id, data_inscricao=date.today())
    inscricao_repo = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False), next_numero_processo=AsyncMock(return_value=saved.numero_processo), save=AsyncMock(return_value=saved))
    escola_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(nome='Escola Teste')))
    citizen_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id)))
    request_service = SimpleNamespace(create_education_request=AsyncMock(return_value=uuid4()), mark_education_request_completed=AsyncMock(return_value=True))
    service = InscricaoService(inscricao_repo=inscricao_repo, escola_repo=escola_repo, citizen_repo=citizen_repo, request_service=request_service)
    result = asyncio.run(service.criar_inscricao_basica(citizen_id=citizen_id, escola_id=escola_id))
    assert result.id == saved.id
    citizen_repo.get_by_id.assert_awaited_once_with(citizen_id)
    escola_repo.get_by_id.assert_awaited_once_with(escola_id)
    request_service.create_education_request.assert_awaited_once()