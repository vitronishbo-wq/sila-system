from app.core.observability import trace
'Attachment service'
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.models.attachment import Attachment
from ..infrastructure.repositories.attachment_repository import AttachmentRepository
from ..infrastructure.repositories.event_repository import EventRepository
from ..domain.models.request_event import RequestEvent

class AttachmentService:
    """Service for managing attachments"""

    def __init__(self, db: AsyncSession, attachment_repo: AttachmentRepository, event_repo: EventRepository):
        self.db = db
        self.attachment_repo = attachment_repo
        self.event_repo = event_repo

    @trace()
    async def upload_attachment(self, request_id: UUID, filename: str, content_type: str, storage_url: str, uploaded_by: UUID, size_bytes: int=0) -> Attachment:
        """Upload attachment and record event"""
        attachment = Attachment(request_id=request_id, filename=filename, content_type=content_type, storage_url=storage_url, uploaded_by=uploaded_by, size_bytes=size_bytes)
        saved = await self.attachment_repo.save(attachment)
        event = RequestEvent(request_id=request_id, event_type='ATTACHMENT_ADDED', payload={'attachment_id': str(saved.id), 'filename': filename, 'size_bytes': size_bytes}, actor_id=uploaded_by)
        await self.event_repo.save(event)
        return saved

    @trace()
    async def get_attachments(self, request_id: UUID) -> List[Attachment]:
        """Get all attachments for request"""
        return await self.attachment_repo.get_by_request(request_id)

    @trace()
    async def delete_attachment(self, attachment_id: UUID, actor_id: UUID) -> bool:
        """Delete attachment"""
        attachment = await self.attachment_repo.get_by_id(attachment_id)
        if not attachment:
            return False
        success = await self.attachment_repo.delete(attachment_id)
        if success:
            event = RequestEvent(request_id=attachment.request_id, event_type='ATTACHMENT_DELETED', payload={'attachment_id': str(attachment_id)}, actor_id=actor_id)
            await self.event_repo.save(event)
        return success