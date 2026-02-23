from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.modules.workflow.domain.models.workflow_task import WorkflowTask
from app.modules.workflow.domain.enums import TaskStatus, TaskPriority
from app.modules.workflow.infrastructure.models.workflow_task_model import WorkflowTaskModel
from app.modules.workflow.application.ports.task_repository_port import TaskRepositoryPort


class TaskRepository(TaskRepositoryPort):
    """Implementação do repositório de tarefas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_task(self, task: WorkflowTask) -> WorkflowTask:
        model = self._to_model(task)
        existing = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.id == task.id
        ).first()
        
        if existing:
            for key, value in model.__dict__.items():
                if not key.startswith('_'):
                    setattr(existing, key, value)
            self.db.flush()
            return self._to_domain(existing)
        else:
            self.db.add(model)
            self.db.flush()
            return self._to_domain(model)
    
    def get_task(self, task_id: UUID) -> Optional[WorkflowTask]:
        model = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.id == task_id
        ).first()
        return self._to_domain(model) if model else None
    
    def get_tasks_by_instance(self, instance_id: UUID) -> List[WorkflowTask]:
        models = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.instance_id == instance_id
        ).order_by(WorkflowTaskModel.created_at).all()
        return [self._to_domain(m) for m in models]
    
    def get_pending_tasks(self, user_id: UUID = None, role: str = None,
                          skip: int = 0, limit: int = 100) -> Tuple[List[WorkflowTask], int]:
        query = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.status == TaskStatus.PENDING.value
        )
        
        if user_id or role:
            conditions = []
            if user_id:
                conditions.append(WorkflowTaskModel.assigned_to == user_id)
            if role:
                conditions.append(WorkflowTaskModel.assigned_role == role)
            query = query.filter(or_(*conditions))
        
        total = query.count()
        models = query.order_by(
            WorkflowTaskModel.priority.desc(),
            WorkflowTaskModel.due_at
        ).offset(skip).limit(limit).all()
        
        return [self._to_domain(m) for m in models], total
    
    def get_assigned_tasks(self, user_id: UUID, status: TaskStatus = None,
                           skip: int = 0, limit: int = 100) -> Tuple[List[WorkflowTask], int]:
        query = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.assigned_to == user_id
        )
        
        if status:
            query = query.filter(WorkflowTaskModel.status == status.value)
        else:
            query = query.filter(WorkflowTaskModel.status.in_([
                TaskStatus.ASSIGNED.value,
                TaskStatus.IN_PROGRESS.value
            ]))
        
        total = query.count()
        models = query.order_by(
            WorkflowTaskModel.priority.desc(),
            WorkflowTaskModel.due_at
        ).offset(skip).limit(limit).all()
        
        return [self._to_domain(m) for m in models], total
    
    def get_tasks_by_status(self, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[WorkflowTask]:
        models = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.status == status.value
        ).order_by(
            WorkflowTaskModel.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return [self._to_domain(m) for m in models]
    
    def get_overdue_tasks(self) -> List[WorkflowTask]:
        models = self.db.query(WorkflowTaskModel).filter(
            WorkflowTaskModel.due_at < datetime.now(),
            WorkflowTaskModel.status.in_([
                TaskStatus.PENDING.value,
                TaskStatus.ASSIGNED.value,
                TaskStatus.IN_PROGRESS.value
            ])
        ).all()
        
        return [self._to_domain(m) for m in models]
    
    def assign_task(self, task_id: UUID, user_id: UUID) -> WorkflowTask:
        task = self.get_task(task_id)
        if task:
            task.assign(user_id)
            return self.save_task(task)
        return None
    
    def complete_task(self, task_id: UUID, result: dict = None) -> WorkflowTask:
        task = self.get_task(task_id)
        if task:
            task.complete(result)
            return self.save_task(task)
        return None
    
    def _to_domain(self, model: WorkflowTaskModel) -> Optional[WorkflowTask]:
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
            metadata=model.metadata or {},
            updated_at=model.updated_at
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
            metadata=domain.metadata,
            updated_at=domain.updated_at
        )
