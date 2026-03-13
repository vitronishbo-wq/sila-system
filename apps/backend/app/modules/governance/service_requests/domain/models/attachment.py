"""Attachment domain model"""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class Attachment:
    """Attachment entity"""
    request_id: UUID = field()
    filename: str = field()
    content_type: str = field()
    storage_url: str = field()
    uploaded_by: UUID = field()
    id: UUID = field(default_factory=uuid4)
    size_bytes: int = field(default=0)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {'id': str(self.id), 'request_id': str(self.request_id), 'filename': self.filename, 'content_type': self.content_type, 'storage_url': self.storage_url, 'uploaded_by': str(self.uploaded_by), 'size_bytes': self.size_bytes, 'created_at': self.created_at.isoformat()}