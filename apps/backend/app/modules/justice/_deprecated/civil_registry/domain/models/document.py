from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

try:
    from apps.backend.app.modules.justice.bounded_contexts.infrastructure.models.document import Document as _Document
    Document = _Document
except Exception:
    @dataclass
    class Document:
        id: str
        citizen_id: str
        document_type: str
        document_number: str
        issued_at: datetime = field(default_factory=datetime.utcnow)
        expires_at: Optional[datetime] = None

__all__ = ["Document"]
