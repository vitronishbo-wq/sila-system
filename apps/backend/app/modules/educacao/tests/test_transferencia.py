from __future__ import annotations
import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from apps.backend.app.modules.educacao.application.transferencia_service import TransferenciaService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models import Matricula, StatusMatricula, Turma, Turno
from apps.backend.app.modules.educacao.exceptions import TransferenciaDuplicadaError

def _base_fixture():
    citizen_id = uuid4()
    escola_origem_id = uuid4()
    escola_destino_id = uuid4()
    ano_letivo_id = uuid4()
    turma_origem_id = uuid4()
    turma_destino_id = uuid4()
    matricula = Matricula(id=uuid4(), numero_processo='2026/0012/0001', citizen_id=citizen_id, escola_id=escola_origem_id, turma_id=turma_origem_id, ano_letivo_id=ano_letivo_id, data_matricula=date.today(), status=StatusMatricula.ATIVA)
    turma_destino = Turma(id=turma_destino_id, escola_id=escola_destino_id, ano_letivo_id=ano_letivo_id, codigo='7A', classe='7a', turno=Turno.MANHA, capacidade=40, ativa=True)
    return SimpleNamespace(citizen_id=citizen_id, escola_origem_id=escola_origem_id, escola_destino_id=escola_destino_id, ano_letivo_id=ano_letivo_id, turma_origem_id=turma_origem_id, turma_destino_id=turma_destino_id, matricula=matricula, turma_destino=turma_destino)

def test_solicitar_transferencia_fluxo_real() -> None:
    fx = _base_fixture()
    record = SimpleNamespace(id=uuid4(), numero_processo='TRF/TRANSFERENCIA/2026/0001', service_type='transferencia', citizen_id=fx.citizen_id, instituicao_id=fx.escola_destino_id, data_registo=date.today(), status=StatusFluxo.EM_ANALISE, observacoes=None, metadata={})
    repository = SimpleNamespace(get_active_by_matricula=AsyncMock(return_value=None), next_numero_processo=AsyncMock(return_value=record.numero_processo), save=AsyncMock(return_value=record))
    service = TransferenciaService(repository=repository, matricula_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=fx.matricula)), escola_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(nome='Destino'))), turma_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=fx.turma_destino), count_matriculas_ativas=AsyncMock(return_value=10)), citizen_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=fx.citizen_id))), request_service=SimpleNamespace(create_education_request=AsyncMock(return_value=uuid4()), mark_education_request_completed=AsyncMock(return_value=True)))
    created = asyncio.run(service.solicitar_transferencia(matricula_id=fx.matricula.id, escola_destino_id=fx.escola_destino_id, turma_destino_id=fx.turma_destino_id, motivo='Mudanca de endereco'))
    assert created.numero_processo == 'TRF/TRANSFERENCIA/2026/0001'
    assert created.status == StatusFluxo.EM_ANALISE

def test_solicitar_transferencia_bloqueia_duplicada_por_matricula() -> None:
    fx = _base_fixture()
    repository = SimpleNamespace(get_active_by_matricula=AsyncMock(return_value=SimpleNamespace(id=uuid4())), next_numero_processo=AsyncMock(), save=AsyncMock())
    service = TransferenciaService(repository=repository, matricula_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=fx.matricula)), escola_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(nome='Destino'))), turma_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=fx.turma_destino), count_matriculas_ativas=AsyncMock(return_value=2)), citizen_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=fx.citizen_id))), request_service=SimpleNamespace(create_education_request=AsyncMock()))
    try:
        asyncio.run(service.solicitar_transferencia(matricula_id=fx.matricula.id, escola_destino_id=fx.escola_destino_id, turma_destino_id=fx.turma_destino_id, motivo='Mudanca'))
        assert False, 'Esperava TransferenciaDuplicadaError'
    except TransferenciaDuplicadaError:
        assert True

def test_aprovar_transferencia_cria_nova_matricula_e_encerra_antiga() -> None:
    fx = _base_fixture()
    transferencia = SimpleNamespace(id=uuid4(), numero_processo='TRF/TRANSFERENCIA/2026/0002', service_type='transferencia', citizen_id=fx.citizen_id, instituicao_id=fx.escola_destino_id, data_registo=date.today(), status=StatusFluxo.EM_ANALISE, observacoes=None, metadata={'matricula_origem_id': str(fx.matricula.id), 'escola_origem_id': str(fx.escola_origem_id), 'turma_origem_id': str(fx.turma_origem_id), 'escola_destino_id': str(fx.escola_destino_id), 'turma_destino_id': str(fx.turma_destino_id), 'ano_letivo_id': str(fx.ano_letivo_id)})
    saved_records: list[Matricula] = []

    async def save_matricula(item: Matricula) -> Matricula:
        saved_records.append(item)
        return item
    service = TransferenciaService(repository=SimpleNamespace(get_by_id=AsyncMock(return_value=transferencia), save=AsyncMock(side_effect=lambda item: item)), matricula_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=fx.matricula), save=AsyncMock(side_effect=save_matricula), next_numero_processo=AsyncMock(return_value='2026/0007/0042')), escola_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(nome='Destino'))), turma_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=fx.turma_destino), count_matriculas_ativas=AsyncMock(return_value=12)), citizen_repo=None, request_service=SimpleNamespace(mark_education_request_completed=AsyncMock(return_value=True)))
    updated = asyncio.run(service.aprovar_transferencia(transferencia_id=transferencia.id, actor_id=uuid4(), resumo='Aprovada pela direcao'))
    assert updated.status == StatusFluxo.APROVADA
    assert len(saved_records) == 2
    assert saved_records[0].status == StatusMatricula.TRANSFERIDA
    assert saved_records[1].status == StatusMatricula.ATIVA
    assert saved_records[1].escola_id == fx.escola_destino_id