from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AuditLogResponse(BaseModel):
    """Schema para log de auditoria"""

    id: UUID
    action: str
    user_id: UUID | None
    entity_id: UUID | None
    entity_type: str
    details: dict[str, Any]
    ip_address: str | None
    user_agent: str | None
    created_at: datetime


class AuditSearchRequest(BaseModel):
    """Schema para pesquisa de auditoria"""

    user_id: UUID | None = None
    entity_id: UUID | None = None
    entity_type: str | None = None
    action: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)


class AuditListResponse(BaseModel):
    """Schema para listagem de auditoria"""

    total: int
    items: list[AuditLogResponse]
