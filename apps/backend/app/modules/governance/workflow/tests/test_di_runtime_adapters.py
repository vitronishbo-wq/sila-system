from __future__ import annotations
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import AsyncMock
import pytest
from app.modules.governance.workflow.api import deps
from app.modules.governance.workflow.application.services.workflow_engine import WorkflowEngine
from app.modules.governance.workflow.domain.models.workflow_definition import WorkflowDefinition
from app.modules.governance.workflow.domain.models.workflow_instance import WorkflowInstance
from app.modules.governance.workflow.domain.models.workflow_state import WorkflowState
from app.modules.governance.workflow.domain.models.workflow_transition import WorkflowTransition
from app.modules.governance.workflow.infrastructure.adapters import AssistenciaSocialAdapter, EducacaoAdapter, EmpregoAdapter, IdentidadeAdapter, JuventudeAdapter, SaudeAdapter

class _EducacaoStub:

    def __init__(self):
        self.calls: list = []

    async def has_matricula_ativa(self, citizen_id):
        self.calls.append(citizen_id)
        return True

class _EmpregoStub:

    async def get_status_candidato(self, citizen_id):
        _ = citizen_id
        return 'ativo'

@pytest.mark.asyncio
async def test_get_workflow_engine_wires_runtime_adapters():
    fake_db = object()
    engine = await deps.get_workflow_engine(db=fake_db)
    assert isinstance(engine, WorkflowEngine)
    assert isinstance(engine.adapters['educacao'], EducacaoAdapter)
    assert isinstance(engine.adapters['identidade'], IdentidadeAdapter)
    assert isinstance(engine.adapters['juventude'], JuventudeAdapter)
    assert isinstance(engine.adapters['emprego'], EmpregoAdapter)
    assert isinstance(engine.adapters['saude'], SaudeAdapter)
    assert isinstance(engine.adapters['assistencia_social'], AssistenciaSocialAdapter)

@pytest.mark.asyncio
async def test_execute_transition_uses_adapter_condition_expression():
    workflow_id = uuid4()
    from_state_id = uuid4()
    to_state_id = uuid4()
    actor_id = uuid4()
    definition = WorkflowDefinition(code='WF_INT', name='Workflow Integracao', entity_type='SERVICE_REQUEST', id=workflow_id)
    instance = WorkflowInstance(workflow_id=workflow_id, current_state_id=from_state_id, entity_type='SERVICE_REQUEST', entity_id=uuid4(), citizen_id=uuid4(), created_by=uuid4())
    transition = WorkflowTransition(workflow_id=workflow_id, from_state_id=from_state_id, to_state_id=to_state_id, code='NEXT', name='Avancar', condition_expression='educacao.has_matricula_ativa')
    to_state = WorkflowState(workflow_id=workflow_id, id=to_state_id, code='DONE', name='Concluido', is_final=True)
    workflow_repo = AsyncMock()
    task_repo = AsyncMock()
    workflow_repo.get_instance.return_value = instance
    workflow_repo.get_definition.return_value = definition
    workflow_repo.get_transition_by_code.return_value = transition
    workflow_repo.save_instance.side_effect = lambda value: value
    workflow_repo.get_state.return_value = to_state
    iam = AsyncMock()
    iam.get_user.return_value = SimpleNamespace(permissions=[], roles=[])
    educacao_stub = _EducacaoStub()
    engine = WorkflowEngine(workflow_repo=workflow_repo, task_repo=task_repo, iam=iam, notifications=SimpleNamespace(notify_citizen=lambda *args, **kwargs: None, notify_operator=lambda *args, **kwargs: None, notify_managers=lambda *args, **kwargs: None), educacao_adapter=educacao_stub)
    result = await engine.execute_transition(instance_id=instance.id, transition_code='NEXT', actor_id=actor_id)
    assert result.is_completed
    assert educacao_stub.calls == [instance.citizen_id]

@pytest.mark.asyncio
async def test_execute_transition_runs_adapter_action_and_stores_result():
    workflow_id = uuid4()
    from_state_id = uuid4()
    to_state_id = uuid4()
    actor_id = uuid4()
    definition = WorkflowDefinition(code='WF_ACT', name='Workflow Actions', entity_type='SERVICE_REQUEST', id=workflow_id)
    instance = WorkflowInstance(workflow_id=workflow_id, current_state_id=from_state_id, entity_type='SERVICE_REQUEST', entity_id=uuid4(), citizen_id=uuid4(), created_by=uuid4())
    transition = WorkflowTransition(workflow_id=workflow_id, from_state_id=from_state_id, to_state_id=to_state_id, code='NEXT', name='Avancar', post_actions={'call_adapter': {'adapter': 'emprego', 'method': 'get_status_candidato', 'args': {'citizen_id': '$citizen_id'}, 'save_as': 'status_emprego'}})
    to_state = WorkflowState(workflow_id=workflow_id, id=to_state_id, code='IN_PROGRESS', name='Em andamento')
    workflow_repo = AsyncMock()
    task_repo = AsyncMock()
    workflow_repo.get_instance.return_value = instance
    workflow_repo.get_definition.return_value = definition
    workflow_repo.get_transition_by_code.return_value = transition
    workflow_repo.save_instance.side_effect = lambda value: value
    workflow_repo.get_state.return_value = to_state
    iam = AsyncMock()
    iam.get_user.return_value = SimpleNamespace(permissions=[], roles=[])
    engine = WorkflowEngine(workflow_repo=workflow_repo, task_repo=task_repo, iam=iam, notifications=SimpleNamespace(notify_citizen=lambda *args, **kwargs: None, notify_operator=lambda *args, **kwargs: None, notify_managers=lambda *args, **kwargs: None), emprego_adapter=_EmpregoStub())
    await engine.execute_transition(instance_id=instance.id, transition_code='NEXT', actor_id=actor_id)
    assert instance.get_variable('status_emprego') == 'ativo'