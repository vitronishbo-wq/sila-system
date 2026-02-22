from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class TaskResponse(BaseModel):
    """Response de tarefa"""
    id: UUID
    instance_id: UUID
    title: str
    description: Optional[str]
    assigned_to: Optional[UUID]
    assigned_role: Optional[str]
    status: str
    priority: str
    form_data: Dict[str, Any]
    created_at: datetime
    due_at: Optional[datetime]
    is_overdue: bool


class TaskAssignRequest(BaseModel):
    """Request para atribuir tarefa"""
    user_id: UUID = Field(..., description="ID do usuário")


class TaskCompleteRequest(BaseModel):
    """Request para completar tarefa"""
    result: Dict[str, Any] = Field(default_factory=dict)
    comment: Optional[str] = None


class TaskListResponse(BaseModel):
    """Response para listagem de tarefas"""
    total: int
    items: List[TaskResponse]
