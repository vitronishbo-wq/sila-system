from __future__ import annotations
import asyncio
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
from apps.backend.app.modules.educacao.domain.models import CicloEnsino, Turma, Turno
from apps.backend.app.modules.educacao.domain.models.matricula import StatusMatricula
from apps.backend.app.modules.educacao.exceptions import IdadeMinimaNaoAtendidaError, TurmaSemVagasError

def _build_service(*, turma: Turma, citizen_birth_date: date, ocupacao: int) -> MatriculaService:
    matricula_repo = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False), next_numero_processo=AsyncMock(return_value='2026/0012/0001'), save=AsyncMock(side_effect=lambda matricula: matricula))
    turma_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=turma), count_matriculas_ativas=AsyncMock(return_value=ocupacao))
    escola_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=turma.escola_id, nome='Escola Integrada', ciclos=[CicloEnsino.PRIMARIO])))
    citizen_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(citizen_id=uuid4(), birth_date=citizen_birth_date)))
    request_service = SimpleNamespace(create_education_request=AsyncMock(return_value=uuid4()), mark_education_request_completed=AsyncMock(return_value=True))
    return MatriculaService(matricula_repo=matricula_repo, turma_repo=turma_repo, escola_repo=escola_repo, citizen_repo=citizen_repo, request_service=request_service)

def test_criar_matricula_rejeita_idade_abaixo_minimo() -> None:
    escola_id = uuid4()
    turma = Turma(id=uuid4(), escola_id=escola_id, ano_letivo_id=uuid4(), codigo='1A', classe='1a', turno=Turno.MANHA, capacidade=40, ativa=True)
    service = _build_service(turma=turma, citizen_birth_date=date.today() - timedelta(days=365 * 5), ocupacao=0)
    try:
        asyncio.run(service.criar_matricula(citizen_id=uuid4(), escola_id=escola_id, turma_id=turma.id, ano_letivo_id=turma.ano_letivo_id))
        assert False, 'Esperava IdadeMinimaNaoAtendidaError'
    except IdadeMinimaNaoAtendidaError:
        assert True

def test_criar_matricula_rejeita_turma_sem_vagas() -> None:
    escola_id = uuid4()
    turma = Turma(id=uuid4(), escola_id=escola_id, ano_letivo_id=uuid4(), codigo='7A', classe='7a', turno=Turno.MANHA, capacidade=1, ativa=True)
    service = _build_service(turma=turma, citizen_birth_date=date.today() - timedelta(days=365 * 14), ocupacao=1)
    try:
        asyncio.run(service.criar_matricula(citizen_id=uuid4(), escola_id=escola_id, turma_id=turma.id, ano_letivo_id=turma.ano_letivo_id))
        assert False, 'Esperava TurmaSemVagasError'
    except TurmaSemVagasError:
        assert True

def test_criar_matricula_aplica_regras_e_rastreia_request() -> None:
    escola_id = uuid4()
    citizen_id = uuid4()
    turma = Turma(id=uuid4(), escola_id=escola_id, ano_letivo_id=uuid4(), codigo='7A', classe='7a', turno=Turno.MANHA, capacidade=30, ativa=True)
    service = _build_service(turma=turma, citizen_birth_date=date.today() - timedelta(days=365 * 15), ocupacao=4)
    matricula = asyncio.run(service.criar_matricula(citizen_id=citizen_id, escola_id=escola_id, turma_id=turma.id, ano_letivo_id=turma.ano_letivo_id))
    assert matricula.status == StatusMatricula.PENDENTE
    assert matricula.turma_id == turma.id
    service.request_service.create_education_request.assert_awaited_once()
