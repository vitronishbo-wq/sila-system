"""Attachment schema"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class AttachmentUploadRequest(BaseModel):
    """Schema for attachment upload"""
    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str = Field(..., max_length=100)
    storage_url: str = Field(...)

class AttachmentResponse(BaseModel):
    """Schema for attachment response"""
    id: UUID
    request_id: UUID
    filename: str
    content_type: str
    storage_url: str
    uploaded_by: UUID
    size_bytes: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AttachmentListResponse(BaseModel):
    """Schema for attachment list"""
    attachments: list[AttachmentResponse]
    total: int