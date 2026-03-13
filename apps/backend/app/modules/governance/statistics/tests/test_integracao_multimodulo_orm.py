from __future__ import annotations
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import uuid4
import pytest
from sqlalchemy import func, select, text
from apps.backend.app.domain.bridges.identity_bridge import BIEventRecord, BIRecord, CitizenFUC
from apps.backend.app.domain.bridges.society_statistics_models_bridge import AppointmentModel, BeneficiarioModel, BeneficioModel, CadastroUnicoModel, CandidatoModel, ContratoModel, InternamentoModel, JovemModel, MatriculaModel, OfertaModel, ProgramaJuvenilModel, TurmaModel, VaccineDoseModel
from apps.backend.app.modules.governance.service_requests.infrastructure.models.service_request_model import ServiceRequestModel
from apps.backend.app.modules.governance.statistics.api.deps import get_statistics_service
from apps.backend.app.modules.governance.statistics.application.services.statistics_service import StatisticsService
from apps.backend.app.modules.governance.statistics.infrastructure.models.statistic_model import StatisticModel
from apps.backend.app.modules.governance.statistics.infrastructure.models.timeseries_model import TimeSeriesModel
from apps.backend.app.modules.governance.statistics.infrastructure.repositories.statistics_repository import StatisticsRepository
from apps.backend.app.modules.governance.statistics.integrations.data_sources import DataSources
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_definition_model import WorkflowDefinitionModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_instance_model import WorkflowInstanceModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_task_model import WorkflowTaskModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_transition_model import WorkflowTransitionModel
SOURCE_REQUIREMENTS = {'educacao': {'educacao_turmas', 'educacao_matriculas'}, 'juventude': {'juventude_jovens', 'juventude_programas'}, 'emprego': {'emprego_candidatos', 'emprego_ofertas', 'emprego_contratos'}, 'saude': {'appointments', 'vaccine_doses', 'health_internamentos'}, 'assistencia': {'assistencia_social_beneficiarios', 'assistencia_social_beneficios', 'assistencia_social_cadastros_unicos'}, 'identidade': {'citizen_fuc', 'bi_records', 'bi_events'}, 'workflow': {'wf_definitions', 'wf_states', 'wf_transitions', 'wf_instances', 'wf_tasks'}, 'service_requests': {'service_requests'}}

async def _available_tables(db_session, table_names: set[str]) -> set[str]:
    available: set[str] = set()
    for table_name in table_names:
        result = await db_session.execute(text('SELECT to_regclass(:table_name)'), {'table_name': f'public.{table_name}'})
        if result.scalar() is not None:
            available.add(table_name)
    return available

async def _seed_for_available_sources(db_session, available: set[str]) -> set[str]:
    today = date.today()
    seeded_sources: set[str] = set()
    citizen_id = uuid4()
    if 'citizen_fuc' in available:
        db_session.add(CitizenFUC(citizen_id=citizen_id, full_name='Cidadao Statistics Integracao', is_active=True, vital_status='alive', document_number=f'BI-{citizen_id.hex[:8]}'))
    if SOURCE_REQUIREMENTS['identidade'].issubset(available):
        db_session.add(BIRecord(citizen_fuc_id=str(citizen_id), bi_number=f'{uuid4().hex[:12].upper()}', issue_date=today - timedelta(days=30), expiry_date=today + timedelta(days=365), status='active', version=1, reason_for_status=None))
        db_session.add(BIEventRecord(aggregate_id=str(citizen_id), event_type='BI_ISSUED', operator_id='stats-test', payload={'ok': True}, event_metadata={}))
        seeded_sources.add('identidade')
    if SOURCE_REQUIREMENTS['educacao'].issubset(available):
        escola_id = uuid4()
        turma_id = uuid4()
        ano_letivo_id = uuid4()
        db_session.add(TurmaModel(id=turma_id, escola_id=escola_id, ano_letivo_id=ano_letivo_id, codigo=f'TURMA-{uuid4().hex[:6]}', classe='10A', turno='manha', capacidade=30, ativa=True))
        db_session.add(MatriculaModel(id=uuid4(), numero_processo=f'MAT-{uuid4().hex[:10]}', citizen_id=citizen_id, escola_id=escola_id, turma_id=turma_id, ano_letivo_id=ano_letivo_id, data_matricula=today, status='ativa', observacoes=None))
        seeded_sources.add('educacao')
    if SOURCE_REQUIREMENTS['juventude'].issubset(available):
        db_session.add(JovemModel(id=uuid4(), numero_registro=f'JOV-{uuid4().hex[:8]}', nome='Jovem Statistics', data_nascimento=date(today.year - 20, 1, 1), faixa_etaria='18_24', genero='M', naturalidade='Huambo', nacionalidade='Angolana', escolaridade='medio_completo', situacao_ocupacional='procura_emprego', endereco='Rua A', municipio='Huambo', provincia='Huambo', citizen_id=citizen_id, data_cadastro=today, ativo=True, acompanhamento_psicossocial=True))
        db_session.add(ProgramaJuvenilModel(id=uuid4(), codigo_programa=f'PRG-{uuid4().hex[:8]}', nome='Programa Integracao Statistics', tipo='capacitacao', data_inicio=today - timedelta(days=5), data_fim=None, vagas=100, municipio='Huambo', provincia='Huambo', status='ativo', data_cadastro=today, ativo=True))
        seeded_sources.add('juventude')
    if SOURCE_REQUIREMENTS['emprego'].issubset(available):
        db_session.add(CandidatoModel(id=uuid4(), numero_processo=f'CAND-{uuid4().hex[:8]}', citizen_id=citizen_id, data_registro=today, escolaridade='secundaria', situacao='desempregado', areas_interesse=['tecnologia'], experiencias=[], habilidades=['python'], status='ativo', observacoes=None))
        db_session.add(OfertaModel(id=uuid4(), numero_processo=f'OF-{uuid4().hex[:8]}', citizen_id=citizen_id, data_registro=today, service_type='vaga_emprego', status='aberta', observacoes=None, metadata_json={}))
        db_session.add(ContratoModel(id=uuid4(), numero_processo=f'CON-{uuid4().hex[:8]}', citizen_id=citizen_id, data_registro=today, service_type='contratacao', status='ativo', observacoes=None, metadata_json={}))
        seeded_sources.add('emprego')
    if SOURCE_REQUIREMENTS['saude'].issubset(available):
        health_unit_id = uuid4()
        db_session.add(AppointmentModel(id=uuid4(), appointment_number=f'APT-{uuid4().hex[:8]}', citizen_id=citizen_id, created_by=uuid4(), doctor_id=None, health_unit_id=health_unit_id, appointment_type='consulta', specialty='clinica_geral', appointment_date=today, appointment_time=time(10, 0), duration_minutes=30, status='completed', priority='MEDIA', reason='Rotina', symptoms=None, notes=None, workflow_instance_id=None, workflow_data={}, metadata_={}, tags=[]))
        db_session.add(VaccineDoseModel(id=uuid4(), citizen_id=citizen_id, vaccine_id=uuid4(), health_unit_id=health_unit_id, applied_by=uuid4(), dose_number=1, batch_number=f'LOT-{uuid4().hex[:8]}', application_date=today, next_dose_date=None, status='applied', adverse_reactions=None, metadata_={}))
        db_session.add(InternamentoModel(id=uuid4(), citizen_id=citizen_id, created_by=uuid4(), health_unit_id=health_unit_id, reason='Observacao', status='admitted', bed_number=None, expected_discharge_at=None, admitted_at=datetime.utcnow(), observed_at=None, discharged_at=None, transferred_at=None, transfer_to_unit_id=None, discharge_summary=None, cancellation_reason=None, cancelled_at=None))
        seeded_sources.add('saude')
    if SOURCE_REQUIREMENTS['assistencia'].issubset(available):
        cadastro_id = uuid4()
        beneficiario_id = uuid4()
        db_session.add(CadastroUnicoModel(id=cadastro_id, codigo=f'CAD-{uuid4().hex[:8]}', citizen_id_responsavel=citizen_id, renda_per_capita=Decimal('180.00'), composicao_familiar=[], condicoes_moradia='ALUGADA', acesso_agua=True, acesso_energia=True, status='ativo', data_cadastro=today, observacoes=None))
        db_session.add(BeneficiarioModel(id=beneficiario_id, numero_registro=f'BEN-{uuid4().hex[:8]}', citizen_id=citizen_id, cadastro_unico_id=cadastro_id, faixa_vulnerabilidade='alta', situacao='ativo', data_cadastro=today, observacoes=None, ativo=True))
        db_session.add(BeneficioModel(id=uuid4(), codigo=f'BFC-{uuid4().hex[:8]}', beneficiario_id=beneficiario_id, programa_social_id=None, tipo='bpc_pcd', valor=Decimal('706.00'), status='aprovado', data_solicitacao=today, data_concessao=today, data_fim=None, motivo_status=None))
        seeded_sources.add('assistencia')
    if SOURCE_REQUIREMENTS['workflow'].issubset(available):
        workflow_id = uuid4()
        state_id = uuid4()
        transition_id = uuid4()
        instance_id = uuid4()
        db_session.add(WorkflowDefinitionModel(id=workflow_id, code=f'WF-{uuid4().hex[:8]}', name='Workflow Statistics', description='Integracao statistics', version=1, entity_type='service_request', is_active=True, is_public=False, timeout_hours=None, definition_metadata={}, tags=[], created_by=uuid4()))
        db_session.add(WorkflowStateModel(id=state_id, workflow_id=workflow_id, code='INICIO', name='Inicio', description=None, is_initial=True, is_final=False, is_auto_forward=False, timeout_hours=None, form_schema=None, state_metadata={}))
        db_session.add(WorkflowTransitionModel(id=transition_id, workflow_id=workflow_id, from_state_id=state_id, to_state_id=state_id, code='T1', name='Transicao', description=None, transition_type='USER', assignment_type='ROLE', assignment_value=None, condition_expression=None, required_permissions=[], required_roles=[], pre_actions={}, post_actions={}, transition_metadata={}))
        db_session.add(WorkflowInstanceModel(id=instance_id, workflow_id=workflow_id, current_state_id=state_id, entity_type='service_request', entity_id=uuid4(), citizen_id=citizen_id, created_by=uuid4(), assigned_to=None, status='ACTIVE', variables={}, context={}, started_at=datetime.utcnow() - timedelta(hours=2), completed_at=datetime.utcnow() - timedelta(hours=1), deadline=None, timeout_hours=None, instance_metadata={}, updated_at=None))
        db_session.add(WorkflowTaskModel(id=uuid4(), instance_id=instance_id, state_id=state_id, transition_id=transition_id, title='Task Statistics', description=None, assigned_to=None, assigned_role='OPERADOR', assignment_type='ROLE', status='PENDING', priority='MEDIUM', form_data={}, result_data={}, due_at=None, timeout_hours=None, task_metadata={}))
        seeded_sources.add('workflow')
    if SOURCE_REQUIREMENTS['service_requests'].issubset(available):
        db_session.add(ServiceRequestModel(id=uuid4(), request_number=f'REQ-{uuid4().hex[:8]}', citizen_id=citizen_id, created_by_user_id=uuid4(), assigned_to_user_id=None, service_type='education_enrollment', title='Pedido teste statistics', description='Integracao real', status='completed', priority='MEDIUM', channel='WEB', workflow_instance_id=None, workflow_data={}, metadata_={}, tags=[], submitted_at=datetime.utcnow(), completed_at=datetime.utcnow(), deadline=None, sla_due_at=None, sla_breached=False))
        seeded_sources.add('service_requests')
    await db_session.flush()
    return seeded_sources

@pytest.mark.asyncio
@pytest.mark.integration
async def test_data_sources_collect_metrics_with_real_orm(db_session) -> None:
    required_tables = set().union(*SOURCE_REQUIREMENTS.values())
    available = await _available_tables(db_session, required_tables)
    seeded_sources = await _seed_for_available_sources(db_session, available)
    if not seeded_sources:
        pytest.skip('Nenhuma fonte com schema completo disponível para teste ORM real.')
    sources = DataSources.from_session(db_session).as_dict()
    tested = 0
    for source_name in seeded_sources:
        metrics = await sources[source_name].collect_metrics(date.today())
        assert isinstance(metrics, dict)
        assert metrics
        tested += 1
    assert tested == len(seeded_sources)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_statistics_service_collect_with_real_repo_partial_schema(db_session) -> None:
    required_tables = set().union(*SOURCE_REQUIREMENTS.values(), {'statistics', 'statistics_timeseries'})
    available = await _available_tables(db_session, required_tables)
    seeded_sources = await _seed_for_available_sources(db_session, available)
    if not seeded_sources:
        pytest.skip('Nenhuma fonte com schema completo disponível para teste ORM real.')
    repository = StatisticsRepository(db_session)
    sources = DataSources.from_session(db_session).as_dict()
    service = StatisticsService(repository=repository, data_sources=sources)
    result = await service.collect_all_metrics(date.today())
    assert set(result.keys()) == set(SOURCE_REQUIREMENTS.keys())
    successful_sources = {name for name, payload in result.items() if payload['status'] == 'success'}
    assert successful_sources
    assert successful_sources.intersection(seeded_sources)
    has_statistics_tables = {'statistics', 'statistics_timeseries'}.issubset(available)
    if has_statistics_tables:
        persisted_success = [payload.get('persisted', False) for payload in result.values() if payload['status'] == 'success']
        assert any(persisted_success)
        stats_total = int((await db_session.execute(select(func.count()).select_from(StatisticModel))).scalar() or 0)
        ts_total = int((await db_session.execute(select(func.count()).select_from(TimeSeriesModel))).scalar() or 0)
        assert stats_total > 0
        assert ts_total > 0

@pytest.mark.asyncio
@pytest.mark.integration
async def test_di_wiring_builds_statistics_service_with_all_sources(db_session) -> None:
    service = get_statistics_service(session=db_session)
    assert isinstance(service, StatisticsService)
    assert set(service.data_sources.keys()) == {'educacao', 'juventude', 'emprego', 'saude', 'assistencia', 'identidade', 'workflow', 'service_requests'}