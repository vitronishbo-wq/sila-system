from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class AuditLogResponse(BaseModel):
    """Schema para log de auditoria"""
    id: UUID
    action: str
    user_id: Optional[UUID]
    entity_id: Optional[UUID]
    entity_type: str
    details: Dict[str, Any]
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: datetime

class AuditSearchRequest(BaseModel):
    """Schema para pesquisa de auditoria"""
    user_id: Optional[UUID] = None
    entity_id: Optional[UUID] = None
    entity_type: Optional[str] = None
    action: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)

class AuditListResponse(BaseModel):
    """Schema para listagem de auditoria"""
    total: int
    items: List[AuditLogResponse]