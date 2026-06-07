from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkflowStartRequest(BaseModel):
    """Request para iniciar workflow"""

    workflow_code: str = Field(..., description="Código do workflow")
    entity_type: str = Field(..., description="Tipo de entidade")
    entity_id: UUID = Field(..., description="ID da entidade")
    variables: dict[str, Any] | None = None


class WorkflowTransitionRequest(BaseModel):
    """Request para executar transição"""

    transition_code: str = Field(..., description="Código da transição")
    form_data: dict[str, Any] | None = None
    comment: str | None = None


class WorkflowInstanceResponse(BaseModel):
    """Response de instância de workflow"""

    id: UUID
    workflow_id: UUID
    current_state_id: UUID
    entity_type: str
    entity_id: UUID
    citizen_id: UUID
    status: str
    variables: dict[str, Any]
    started_at: datetime
    completed_at: datetime | None
    deadline: datetime | None
    is_active: bool
    is_overdue: bool
    model_config = ConfigDict(from_attributes=True)


class WorkflowDefinitionResponse(BaseModel):
    """Response de definição de workflow"""

    id: UUID
    code: str
    name: str
    description: str | None
    version: int
    entity_type: str
    is_active: bool
    tags: list[str]
    created_at: datetime


class WorkflowStateResponse(BaseModel):
    """Response de estado"""

    id: UUID
    code: str
    name: str
    is_initial: bool
    is_final: bool
    form_schema: dict[str, Any] | None


class WorkflowTransitionResponse(BaseModel):
    """Response de transição"""

    id: UUID
    code: str
    name: str
    description: str | None
    from_state_id: UUID
    to_state_id: UUID
    transition_type: str
    required_roles: list[str]
    required_permissions: list[str]


class WorkflowHistoryResponse(BaseModel):
    """Response de histórico"""

    id: UUID
    action: str
    action_type: str
    performed_by: UUID | None
    comment: str | None
    data: dict[str, Any]
    created_at: datetime
