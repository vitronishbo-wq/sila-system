from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.governance.workflow.application.ports.task_repository_port import (
    TaskRepositoryPort,
)
from apps.backend.app.modules.governance.workflow.domain.enums import TaskPriority, TaskStatus
from apps.backend.app.modules.governance.workflow.domain.models.workflow_task import WorkflowTask
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_task_model import (
    WorkflowTaskModel,
)


class TaskRepository(TaskRepositoryPort):
    """Implementação async do repositório de tarefas."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_task(self, task: WorkflowTask) -> WorkflowTask:
        model = self._to_model(task)
        existing = await self._get_model(task.id)
        if existing:
            self._copy_model_fields(existing, model)
            await self.db.flush()
            return self._to_domain(existing)
        self.db.add(model)
        await self.db.flush()
        return self._to_domain(model)

    async def get_task(self, task_id: UUID) -> WorkflowTask | None:
        model = await self._get_model(task_id)
        return self._to_domain(model) if model else None

    async def get_tasks_by_instance(self, instance_id: UUID) -> list[WorkflowTask]:
        stmt = (
            select(WorkflowTaskModel)
            .where(WorkflowTaskModel.instance_id == instance_id)
            .order_by(WorkflowTaskModel.created_at)
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_pending_tasks(
        self, user_id: UUID = None, role: str = None, skip: int = 0, limit: int = 100
    ) -> tuple[list[WorkflowTask], int]:
        conditions = [WorkflowTaskModel.status == TaskStatus.PENDING.value]
        if user_id or role:
            role_conditions = []
            if user_id:
                role_conditions.append(WorkflowTaskModel.assigned_to == user_id)
            if role:
                role_conditions.append(WorkflowTaskModel.assigned_role == role)
            conditions.append(or_(*role_conditions))
        base_stmt = select(WorkflowTaskModel).where(and_(*conditions))
        total_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = int((await self.db.execute(total_stmt)).scalar() or 0)
        stmt = (
            base_stmt.order_by(desc(WorkflowTaskModel.priority), WorkflowTaskModel.due_at)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return ([self._to_domain(m) for m in result.scalars().all()], total)

    async def get_assigned_tasks(
        self, user_id: UUID, status: TaskStatus = None, skip: int = 0, limit: int = 100
    ) -> tuple[list[WorkflowTask], int]:
        conditions = [WorkflowTaskModel.assigned_to == user_id]
        if status:
            conditions.append(WorkflowTaskModel.status == status.value)
        else:
            conditions.append(
                WorkflowTaskModel.status.in_(
                    [TaskStatus.ASSIGNED.value, TaskStatus.IN_PROGRESS.value]
                )
            )
        base_stmt = select(WorkflowTaskModel).where(and_(*conditions))
        total_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = int((await self.db.execute(total_stmt)).scalar() or 0)
        stmt = (
            base_stmt.order_by(desc(WorkflowTaskModel.priority), WorkflowTaskModel.due_at)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return ([self._to_domain(m) for m in result.scalars().all()], total)

    async def get_tasks_by_status(
        self, status: TaskStatus, skip: int = 0, limit: int = 100
    ) -> list[WorkflowTask]:
        stmt = (
            select(WorkflowTaskModel)
            .where(WorkflowTaskModel.status == status.value)
            .order_by(desc(WorkflowTaskModel.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_overdue_tasks(self) -> list[WorkflowTask]:
        stmt = select(WorkflowTaskModel).where(
            WorkflowTaskModel.due_at < datetime.now(),
            WorkflowTaskModel.status.in_(
                [TaskStatus.PENDING.value, TaskStatus.ASSIGNED.value, TaskStatus.IN_PROGRESS.value]
            ),
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def assign_task(self, task_id: UUID, user_id: UUID) -> WorkflowTask | None:
        task = await self.get_task(task_id)
        if task:
            task.assign(user_id)
            return await self.save_task(task)
        return None

    async def complete_task(self, task_id: UUID, result: dict = None) -> WorkflowTask | None:
        task = await self.get_task(task_id)
        if task:
            task.complete(result)
            return await self.save_task(task)
        return None

    async def _get_model(self, task_id: UUID) -> WorkflowTaskModel | None:
        stmt = select(WorkflowTaskModel).where(WorkflowTaskModel.id == task_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def _copy_model_fields(target, source) -> None:
        for key, value in source.__dict__.items():
            if key.startswith("_"):
                continue
            setattr(target, key, value)

    def _to_domain(self, model: WorkflowTaskModel) -> WorkflowTask | None:
        if not model:
            return None
        return WorkflowTask(
            id=model.id,
            instance_id=model.instance_id,
            state_id=model.state_id,
            transition_id=model.transition_id,
            title=model.title,
            description=model.description,
            assigned_to=model.assigned_to,
            assigned_role=model.assigned_role,
            assignment_type=model.assignment_type,
            status=TaskStatus(model.status),
            priority=TaskPriority(model.priority),
            form_data=model.form_data or {},
            result_data=model.result_data or {},
            created_at=model.created_at,
            started_at=model.started_at,
            completed_at=model.completed_at,
            due_at=model.due_at,
            timeout_hours=model.timeout_hours,
            metadata=model.task_metadata or {},
            updated_at=model.updated_at,
        )

    def _to_model(self, domain: WorkflowTask) -> WorkflowTaskModel:
        return WorkflowTaskModel(
            id=domain.id,
            instance_id=domain.instance_id,
            state_id=domain.state_id,
            transition_id=domain.transition_id,
            title=domain.title,
            description=domain.description,
            assigned_to=domain.assigned_to,
            assigned_role=domain.assigned_role,
            assignment_type=domain.assignment_type,
            status=domain.status.value,
            priority=domain.priority.value,
            form_data=domain.form_data,
            result_data=domain.result_data,
            created_at=domain.created_at,
            started_at=domain.started_at,
            completed_at=domain.completed_at,
            due_at=domain.due_at,
            timeout_hours=domain.timeout_hours,
            task_metadata=domain.metadata,
            updated_at=domain.updated_at,
        )
