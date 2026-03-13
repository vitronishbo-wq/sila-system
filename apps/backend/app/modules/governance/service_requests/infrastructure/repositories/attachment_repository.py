"""Attachment repository implementation"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...domain.models.attachment import Attachment
from ...application.ports.attachment_repository_port import AttachmentRepositoryPort
from ..models.attachment_model import AttachmentModel

class AttachmentRepository(AttachmentRepositoryPort):
    """Attachment repository implementation"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, attachment: Attachment) -> Attachment:
        """Save attachment"""
        model = AttachmentModel(id=attachment.id, request_id=attachment.request_id, filename=attachment.filename, content_type=attachment.content_type, storage_url=attachment.storage_url, uploaded_by=attachment.uploaded_by, size_bytes=attachment.size_bytes)
        self.db.add(model)
        await self.db.flush()
        return attachment

    async def get_by_id(self, attachment_id: UUID) -> Optional[Attachment]:
        """Get attachment by ID"""
        stmt = select(AttachmentModel).where(AttachmentModel.id == attachment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Attachment(id=model.id, request_id=model.request_id, filename=model.filename, content_type=model.content_type, storage_url=model.storage_url, uploaded_by=model.uploaded_by, size_bytes=model.size_bytes, created_at=model.created_at)

    async def get_by_request(self, request_id: UUID) -> List[Attachment]:
        """Get all attachments for a request"""
        stmt = select(AttachmentModel).where(AttachmentModel.request_id == request_id).order_by(AttachmentModel.created_at.desc())
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        attachments = []
        for model in models:
            attachments.append(Attachment(id=model.id, request_id=model.request_id, filename=model.filename, content_type=model.content_type, storage_url=model.storage_url, uploaded_by=model.uploaded_by, size_bytes=model.size_bytes, created_at=model.created_at))
        return attachments

    async def delete(self, attachment_id: UUID) -> bool:
        """Delete attachment"""
        stmt = select(AttachmentModel).where(AttachmentModel.id == attachment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self.db.delete(model)
        await self.db.flush()
        return True