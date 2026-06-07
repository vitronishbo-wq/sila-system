"""Attachment repository port"""

from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.models.attachment import Attachment


class AttachmentRepositoryPort(ABC):
    """Attachment repository interface"""

    @abstractmethod
    async def save(self, attachment: Attachment) -> Attachment:
        """Save attachment"""
        pass

    @abstractmethod
    async def get_by_id(self, attachment_id: UUID) -> Attachment | None:
        """Get attachment by ID"""
        pass

    @abstractmethod
    async def get_by_request(self, request_id: UUID) -> list[Attachment]:
        """Get all attachments for a request"""
        pass

    @abstractmethod
    async def delete(self, attachment_id: UUID) -> bool:
        """Delete attachment"""
        pass
