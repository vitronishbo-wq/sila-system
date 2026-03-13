from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.governance.workflow.application.ports.workflow_repository_port import WorkflowRepositoryPort
from app.modules.governance.workflow.domain.enums import AssignmentType, TransitionType, WorkflowStatus
from app.modules.governance.workflow.domain.models.workflow_definition import WorkflowDefinition
from app.modules.governance.workflow.domain.models.workflow_history import WorkflowHistory
from app.modules.governance.workflow.domain.models.workflow_instance import WorkflowInstance
from app.modules.governance.workflow.domain.models.workflow_state import WorkflowState
from app.modules.governance.workflow.domain.models.workflow_transition import WorkflowTransition
from app.modules.governance.workflow.infrastructure.models.workflow_definition_model import WorkflowDefinitionModel
from app.modules.governance.workflow.infrastructure.models.workflow_history_model import WorkflowHistoryModel
from app.modules.governance.workflow.infrastructure.models.workflow_instance_model import WorkflowInstanceModel
from app.modules.governance.workflow.infrastructure.models.workflow_state_model import WorkflowStateModel
from app.modules.governance.workflow.infrastructure.models.workflow_transition_model import WorkflowTransitionModel

class WorkflowRepository(WorkflowRepositoryPort):
    """Implementação async do repositório de workflows."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self) -> None:
        await self.db.commit()

    async def save_definition(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        model = self._definition_to_model(definition)
        existing = await self._get_model(WorkflowDefinitionModel, definition.id)
        if existing:
            self._copy_model_fields(existing, model)
            await self.db.flush()
            return self._definition_to_domain(existing)
        self.db.add(model)
        await self.db.flush()
        return self._definition_to_domain(model)

    async def get_definition(self, definition_id: UUID) -> Optional[WorkflowDefinition]:
        model = await self._get_model(WorkflowDefinitionModel, definition_id)
        return self._definition_to_domain(model) if model else None

    async def get_definition_by_code(self, code: str, version: int=None) -> Optional[WorkflowDefinition]:
        stmt = select(WorkflowDefinitionModel).where(WorkflowDefinitionModel.code == code.upper())
        if version is not None:
            stmt = stmt.where(WorkflowDefinitionModel.version == version)
        else:
            stmt = stmt.order_by(desc(WorkflowDefinitionModel.version)).limit(1)
        result = await self.db.execute(stmt)
        model = result.scalars().first()
        return self._definition_to_domain(model) if model else None

    async def list_definitions(self, skip: int=0, limit: int=100) -> Tuple[List[WorkflowDefinition], int]:
        total_stmt = select(func.count()).select_from(WorkflowDefinitionModel).where(WorkflowDefinitionModel.is_active)
        total = int((await self.db.execute(total_stmt)).scalar() or 0)
        stmt = select(WorkflowDefinitionModel).where(WorkflowDefinitionModel.is_active).order_by(desc(WorkflowDefinitionModel.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._definition_to_domain(m) for m in models], total)

    async def save_state(self, state: WorkflowState) -> WorkflowState:
        model = self._state_to_model(state)
        existing = await self._get_model(WorkflowStateModel, state.id)
        if existing:
            self._copy_model_fields(existing, model)
            await self.db.flush()
            return self._state_to_domain(existing)
        self.db.add(model)
        await self.db.flush()
        return self._state_to_domain(model)

    async def get_states(self, workflow_id: UUID) -> List[WorkflowState]:
        stmt = select(WorkflowStateModel).where(WorkflowStateModel.workflow_id == workflow_id)
        result = await self.db.execute(stmt)
        return [self._state_to_domain(m) for m in result.scalars().all()]

    async def get_initial_state(self, workflow_id: UUID) -> Optional[WorkflowState]:
        stmt = select(WorkflowStateModel).where(WorkflowStateModel.workflow_id == workflow_id, WorkflowStateModel.is_initial)
        result = await self.db.execute(stmt)
        model = result.scalars().first()
        return self._state_to_domain(model) if model else None

    async def get_state(self, state_id: UUID) -> Optional[WorkflowState]:
        model = await self._get_model(WorkflowStateModel, state_id)
        return self._state_to_domain(model) if model else None

    async def save_transition(self, transition: WorkflowTransition) -> WorkflowTransition:
        model = self._transition_to_model(transition)
        existing = await self._get_model(WorkflowTransitionModel, transition.id)
        if existing:
            self._copy_model_fields(existing, model)
            await self.db.flush()
            return self._transition_to_domain(existing)
        self.db.add(model)
        await self.db.flush()
        return self._transition_to_domain(model)

    async def get_transitions(self, from_state_id: UUID) -> List[WorkflowTransition]:
        stmt = select(WorkflowTransitionModel).where(WorkflowTransitionModel.from_state_id == from_state_id)
        result = await self.db.execute(stmt)
        return [self._transition_to_domain(m) for m in result.scalars().all()]

    async def get_transition(self, transition_id: UUID) -> Optional[WorkflowTransition]:
        model = await self._get_model(WorkflowTransitionModel, transition_id)
        return self._transition_to_domain(model) if model else None

    async def get_transition_by_code(self, workflow_id: UUID, code: str) -> Optional[WorkflowTransition]:
        stmt = select(WorkflowTransitionModel).where(WorkflowTransitionModel.workflow_id == workflow_id, WorkflowTransitionModel.code == code.upper())
        result = await self.db.execute(stmt)
        model = result.scalars().first()
        return self._transition_to_domain(model) if model else None

    async def save_instance(self, instance: WorkflowInstance) -> WorkflowInstance:
        model = self._instance_to_model(instance)
        existing = await self._get_model(WorkflowInstanceModel, instance.id)
        if existing:
            self._copy_model_fields(existing, model)
            await self.db.flush()
            return self._instance_to_domain(existing)
        self.db.add(model)
        await self.db.flush()
        return self._instance_to_domain(model)

    async def get_instance(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        model = await self._get_model(WorkflowInstanceModel, instance_id)
        return self._instance_to_domain(model) if model else None

    async def get_instance_by_entity(self, entity_type: str, entity_id: UUID) -> Optional[WorkflowInstance]:
        stmt = select(WorkflowInstanceModel).where(WorkflowInstanceModel.entity_type == entity_type, WorkflowInstanceModel.entity_id == entity_id)
        result = await self.db.execute(stmt)
        model = result.scalars().first()
        return self._instance_to_domain(model) if model else None

    async def list_instances(self, citizen_id: UUID=None, status: WorkflowStatus=None, skip: int=0, limit: int=100) -> Tuple[List[WorkflowInstance], int]:
        stmt = select(WorkflowInstanceModel)
        if citizen_id:
            stmt = stmt.where(WorkflowInstanceModel.citizen_id == citizen_id)
        if status:
            stmt = stmt.where(WorkflowInstanceModel.status == status.value)
        total_stmt = select(func.count()).select_from(stmt.subquery())
        total = int((await self.db.execute(total_stmt)).scalar() or 0)
        stmt = stmt.order_by(desc(WorkflowInstanceModel.started_at)).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return ([self._instance_to_domain(m) for m in models], total)

    async def update_instance_state(self, instance_id: UUID, state_id: UUID) -> WorkflowInstance:
        instance = await self.get_instance(instance_id)
        if instance:
            instance.current_state_id = state_id
            instance.updated_at = datetime.now()
            return await self.save_instance(instance)
        return None

    async def save_history(self, history: WorkflowHistory) -> WorkflowHistory:
        model = self._history_to_model(history)
        self.db.add(model)
        await self.db.flush()
        return history

    async def get_instance_history(self, instance_id: UUID, limit: int=100) -> List[WorkflowHistory]:
        stmt = select(WorkflowHistoryModel).where(WorkflowHistoryModel.instance_id == instance_id).order_by(WorkflowHistoryModel.created_at).limit(limit)
        result = await self.db.execute(stmt)
        return [self._history_to_domain(m) for m in result.scalars().all()]

    async def _get_model(self, model_cls, item_id: UUID):
        stmt = select(model_cls).where(model_cls.id == item_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def _copy_model_fields(target, source) -> None:
        for key, value in source.__dict__.items():
            if key.startswith('_'):
                continue
            setattr(target, key, value)

    def _definition_to_domain(self, model: WorkflowDefinitionModel) -> Optional[WorkflowDefinition]:
        if not model:
            return None
        return WorkflowDefinition(id=model.id, code=model.code, name=model.name, description=model.description, version=model.version, entity_type=model.entity_type, is_active=model.is_active, is_public=model.is_public, timeout_hours=model.timeout_hours, metadata=model.definition_metadata or {}, tags=model.tags or [], created_at=model.created_at, updated_at=model.updated_at, created_by=model.created_by)

    def _definition_to_model(self, domain: WorkflowDefinition) -> WorkflowDefinitionModel:
        return WorkflowDefinitionModel(id=domain.id, code=domain.code, name=domain.name, description=domain.description, version=domain.version, entity_type=domain.entity_type, is_active=domain.is_active, is_public=domain.is_public, timeout_hours=domain.timeout_hours, definition_metadata=domain.metadata, tags=domain.tags, created_at=domain.created_at, updated_at=domain.updated_at, created_by=domain.created_by)

    def _state_to_domain(self, model: WorkflowStateModel) -> Optional[WorkflowState]:
        if not model:
            return None
        return WorkflowState(id=model.id, workflow_id=model.workflow_id, code=model.code, name=model.name, description=model.description, is_initial=model.is_initial, is_final=model.is_final, is_auto_forward=model.is_auto_forward, timeout_hours=model.timeout_hours, form_schema=model.form_schema, metadata=model.state_metadata or {}, created_at=model.created_at, updated_at=model.updated_at)

    def _state_to_model(self, domain: WorkflowState) -> WorkflowStateModel:
        return WorkflowStateModel(id=domain.id, workflow_id=domain.workflow_id, code=domain.code, name=domain.name, description=domain.description, is_initial=domain.is_initial, is_final=domain.is_final, is_auto_forward=domain.is_auto_forward, timeout_hours=domain.timeout_hours, form_schema=domain.form_schema, state_metadata=domain.metadata, created_at=domain.created_at, updated_at=domain.updated_at)

    def _transition_to_domain(self, model: WorkflowTransitionModel) -> Optional[WorkflowTransition]:
        if not model:
            return None
        return WorkflowTransition(id=model.id, workflow_id=model.workflow_id, from_state_id=model.from_state_id, to_state_id=model.to_state_id, code=model.code, name=model.name, description=model.description, transition_type=TransitionType(model.transition_type), assignment_type=AssignmentType(model.assignment_type), assignment_value=model.assignment_value, condition_expression=model.condition_expression, required_permissions=model.required_permissions or [], required_roles=model.required_roles or [], pre_actions=model.pre_actions or {}, post_actions=model.post_actions or {}, metadata=model.transition_metadata or {}, created_at=model.created_at, updated_at=model.updated_at)

    def _transition_to_model(self, domain: WorkflowTransition) -> WorkflowTransitionModel:
        return WorkflowTransitionModel(id=domain.id, workflow_id=domain.workflow_id, from_state_id=domain.from_state_id, to_state_id=domain.to_state_id, code=domain.code, name=domain.name, description=domain.description, transition_type=domain.transition_type.value, assignment_type=domain.assignment_type.value, assignment_value=domain.assignment_value, condition_expression=domain.condition_expression, required_permissions=domain.required_permissions, required_roles=domain.required_roles, pre_actions=domain.pre_actions, post_actions=domain.post_actions, transition_metadata=domain.metadata, created_at=domain.created_at, updated_at=domain.updated_at)

    def _instance_to_domain(self, model: WorkflowInstanceModel) -> Optional[WorkflowInstance]:
        if not model:
            return None
        return WorkflowInstance(id=model.id, workflow_id=model.workflow_id, current_state_id=model.current_state_id, entity_type=model.entity_type, entity_id=model.entity_id, citizen_id=model.citizen_id, created_by=model.created_by, assigned_to=model.assigned_to, status=WorkflowStatus(model.status), variables=model.variables or {}, context=model.context or {}, started_at=model.started_at, completed_at=model.completed_at, deadline=model.deadline, timeout_hours=model.timeout_hours, metadata=model.instance_metadata or {}, updated_at=model.updated_at)

    def _instance_to_model(self, domain: WorkflowInstance) -> WorkflowInstanceModel:
        return WorkflowInstanceModel(id=domain.id, workflow_id=domain.workflow_id, current_state_id=domain.current_state_id, entity_type=domain.entity_type, entity_id=domain.entity_id, citizen_id=domain.citizen_id, created_by=domain.created_by, assigned_to=domain.assigned_to, status=domain.status.value, variables=domain.variables, context=domain.context, started_at=domain.started_at, completed_at=domain.completed_at, deadline=domain.deadline, timeout_hours=domain.timeout_hours, instance_metadata=domain.metadata, updated_at=domain.updated_at)

    def _history_to_domain(self, model: WorkflowHistoryModel) -> Optional[WorkflowHistory]:
        if not model:
            return None
        return WorkflowHistory(id=model.id, instance_id=model.instance_id, from_state_id=model.from_state_id, to_state_id=model.to_state_id, transition_id=model.transition_id, task_id=model.task_id, action=model.action, action_type=model.action_type, performed_by=model.performed_by, performed_by_role=model.performed_by_role, comment=model.comment, data=model.data or {}, metadata=model.history_metadata or {}, created_at=model.created_at)

    def _history_to_model(self, domain: WorkflowHistory) -> WorkflowHistoryModel:
        return WorkflowHistoryModel(id=domain.id, instance_id=domain.instance_id, from_state_id=domain.from_state_id, to_state_id=domain.to_state_id, transition_id=domain.transition_id, task_id=domain.task_id, action=domain.action, action_type=domain.action_type, performed_by=domain.performed_by, performed_by_role=domain.performed_by_role, comment=domain.comment, data=domain.data, history_metadata=domain.metadata, created_at=domain.created_at)