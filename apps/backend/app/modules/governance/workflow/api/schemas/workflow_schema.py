from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class WorkflowStartRequest(BaseModel):
    """Request para iniciar workflow"""
    workflow_code: str = Field(..., description='Código do workflow')
    entity_type: str = Field(..., description='Tipo de entidade')
    entity_id: UUID = Field(..., description='ID da entidade')
    variables: Optional[Dict[str, Any]] = None

class WorkflowTransitionRequest(BaseModel):
    """Request para executar transição"""
    transition_code: str = Field(..., description='Código da transição')
    form_data: Optional[Dict[str, Any]] = None
    comment: Optional[str] = None

class WorkflowInstanceResponse(BaseModel):
    """Response de instância de workflow"""
    id: UUID
    workflow_id: UUID
    current_state_id: UUID
    entity_type: str
    entity_id: UUID
    citizen_id: UUID
    status: str
    variables: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime]
    deadline: Optional[datetime]
    is_active: bool
    is_overdue: bool
    model_config = ConfigDict(from_attributes=True)

class WorkflowDefinitionResponse(BaseModel):
    """Response de definição de workflow"""
    id: UUID
    code: str
    name: str
    description: Optional[str]
    version: int
    entity_type: str
    is_active: bool
    tags: List[str]
    created_at: datetime

class WorkflowStateResponse(BaseModel):
    """Response de estado"""
    id: UUID
    code: str
    name: str
    is_initial: bool
    is_final: bool
    form_schema: Optional[Dict[str, Any]]

class WorkflowTransitionResponse(BaseModel):
    """Response de transição"""
    id: UUID
    code: str
    name: str
    description: Optional[str]
    from_state_id: UUID
    to_state_id: UUID
    transition_type: str
    required_roles: List[str]
    required_permissions: List[str]

class WorkflowHistoryResponse(BaseModel):
    """Response de histórico"""
    id: UUID
    action: str
    action_type: str
    performed_by: Optional[UUID]
    comment: Optional[str]
    data: Dict[str, Any]
    created_at: datetime