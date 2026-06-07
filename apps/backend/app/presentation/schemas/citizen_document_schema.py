from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ...domain.document_type_enum import DocumentTypeEnum


class CitizenDocumentCreateSchema(BaseModel):
    citizen_id: UUID
    type: DocumentTypeEnum
    file_path: str
    version: int = 1


class CitizenDocumentReadSchema(BaseModel):
    id: UUID
    citizen_id: UUID
    type: DocumentTypeEnum
    file_path: str
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
