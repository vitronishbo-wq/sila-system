from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class DocumentBase(BaseModel):
    citizen_id: str
    document_type: str
    file_url: str
    issued_at: datetime | None = None
    valid_until: datetime | None = None

class DocumentOut(DocumentBase):
    id: UUID

    class Config:
        from_attributes = True
__all__ = ['DocumentBase', 'DocumentOut']