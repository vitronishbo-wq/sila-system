from __future__ import annotations
from datetime import date
import os
from uuid import UUID, uuid4
import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from app.api.deps import get_db, get_identity_context
from app.core.bridges.identity_bridge import CitizenFUC
from app.core.identity import IdentityContext
from apps.backend.app.modules.governance.workflow.api.router import router as workflow_router
from apps.backend.app.modules.governance.workflow.domain.models.workflow_definition import WorkflowDefinition
from apps.backend.app.modules.governance.workflow.domain.models.workflow_state import WorkflowState
from apps.backend.app.modules.governance.workflow.domain.models.workflow_transition import WorkflowTransition
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_definition_model import WorkflowDefinitionModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_history_model import WorkflowHistoryModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_instance_model import WorkflowInstanceModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_task_model import WorkflowTaskModel
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_transition_model import WorkflowTransitionModel
from apps.backend.app.modules.governance.workflow.infrastructure.repositories.workflow_repository import WorkflowRepository

def _database_url() -> str:
    url = os.environ.get('DATABASE_URL')
    if not url:
        from app.core.settings import settings
        url = str(settings.DATABASE_URL or '')
    if not url:
        raise RuntimeError('DATABASE_URL é obrigatório para testes de endpoint do workflow.')
    if url.startswith('postgresql://'):
        return url.replace('postgresql://', 'postgresql+asyncpg://', 1)
    return url

@pytest_asyncio.fixture(scope='session')
async def workflow_test_engine():
    from app.core.db import Base, register_models
    register_models()
    registry = getattr(Base, 'registry', None)
    if registry is not None and hasattr(registry, 'configure'):
        registry.configure()
    engine = create_async_engine(_database_url(), echo=False, pool_pre_ping=True, poolclass=NullPool)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope='function')
async def session_factory(workflow_test_engine):
    from app.core.db import Base
    required_tables = [CitizenFUC.__table__, WorkflowDefinitionModel.__table__, WorkflowStateModel.__table__, WorkflowTransitionModel.__table__, WorkflowInstanceModel.__table__, WorkflowTaskModel.__table__, WorkflowHistoryModel.__table__]
    async with workflow_test_engine.begin() as connection:
        await connection.run_sync(lambda sync_connection: Base.metadata.create_all(sync_connection, tables=required_tables, checkfirst=True))
    yield async_sessionmaker(bind=workflow_test_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)

def _build_test_app(*, session_factory: async_sessionmaker[AsyncSession], user_id: UUID, citizen_id: UUID) -> FastAPI:
    app = FastAPI()
    app.include_router(workflow_router, prefix='/api/v1')

    async def _override_get_db():
        async with session_factory() as session:
            yield session

    async def _override_identity_context():
        return IdentityContext({'user_id': str(user_id), 'citizen_id': str(citizen_id), 'email': 'workflow-test@sila.local'})
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_identity_context] = _override_identity_context
    return app

async def _seed_workflow_definition(session_factory: async_sessionmaker[AsyncSession], *, code: str, condition_expression: str | None=None, post_actions: dict | None=None) -> tuple[WorkflowDefinition, WorkflowState, WorkflowState]:
    async with session_factory() as session:
        repo = WorkflowRepository(session)
        definition = WorkflowDefinition(code=code, name=f'Workflow {code}', entity_type='SERVICE_REQUEST')
        start_state = WorkflowState(workflow_id=definition.id, code='INICIO', name='Inicio', is_initial=True)
        end_state = WorkflowState(workflow_id=definition.id, code='FIM', name='Fim', is_final=True)
        await repo.save_definition(definition)
        await repo.save_state(start_state)
        await repo.save_state(end_state)
        if condition_expression or post_actions:
            transition = WorkflowTransition(workflow_id=definition.id, from_state_id=start_state.id, to_state_id=end_state.id, code='AVANCAR', name='Avancar', condition_expression=condition_expression, post_actions=post_actions or {})
            await repo.save_transition(transition)
        await repo.commit()
    return (definition, start_state, end_state)

async def _seed_citizen(session_factory: async_sessionmaker[AsyncSession], citizen_id: UUID) -> None:
    async with session_factory() as session:
        session.add(CitizenFUC(citizen_id=citizen_id, full_name='Cidadao Workflow', birth_date=date(1998, 5, 1), gender='M', is_active=True, document_number=f'BI-{citizen_id.hex[:12]}', vital_status='alive'))
        await session.commit()

@pytest.mark.asyncio
async def test_start_workflow_endpoint_with_testclient(session_factory: async_sessionmaker[AsyncSession]):
    user_id = uuid4()
    citizen_id = uuid4()
    definition, _, _ = await _seed_workflow_definition(session_factory, code=f'WF_START_{uuid4().hex[:6]}')
    app = _build_test_app(session_factory=session_factory, user_id=user_id, citizen_id=citizen_id)
    with TestClient(app) as client:
        response = client.post('/api/v1/workflow/start', json={'workflow_code': definition.code, 'entity_type': 'SERVICE_REQUEST', 'entity_id': str(uuid4()), 'variables': {'origem': 'endpoint-test'}})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload['workflow_id'] == str(definition.id)
    assert payload['citizen_id'] == str(citizen_id)
    assert payload['variables']['origem'] == 'endpoint-test'
    assert payload['status'] == 'active'

@pytest.mark.asyncio
async def test_transition_endpoint_applies_condition_expression_and_call_adapter(session_factory: async_sessionmaker[AsyncSession]):
    user_id = uuid4()
    citizen_id = uuid4()
    await _seed_citizen(session_factory, citizen_id)
    definition, _, end_state = await _seed_workflow_definition(session_factory, code=f'WF_TRANS_{uuid4().hex[:6]}', condition_expression='identidade.validar_cidadao_ativo', post_actions={'call_adapter': {'adapter': 'identidade', 'method': 'validar_cidadao_ativo', 'args': {'citizen_id': '$citizen_id'}, 'save_as': 'cidadao_ativo'}})
    app = _build_test_app(session_factory=session_factory, user_id=user_id, citizen_id=citizen_id)
    with TestClient(app) as client:
        start_response = client.post('/api/v1/workflow/start', json={'workflow_code': definition.code, 'entity_type': 'SERVICE_REQUEST', 'entity_id': str(uuid4()), 'variables': {}})
        assert start_response.status_code == 200, start_response.text
        instance_id = start_response.json()['id']
        transition_response = client.post(f'/api/v1/workflow/instances/{instance_id}/transitions', json={'transition_code': 'AVANCAR', 'form_data': {}})
    assert transition_response.status_code == 200
    payload = transition_response.json()
    assert payload['current_state_id'] == str(end_state.id)
    assert payload['status'] == 'completed'
    assert payload['variables']['cidadao_ativo'] is True