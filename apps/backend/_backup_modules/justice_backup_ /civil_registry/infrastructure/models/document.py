import uuid
import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

class DocumentStatus(str, enum.Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class DocumentType(str, enum.Enum):
    BIRTH_CERT = 'birth_cert'
    ID_CARD = 'id_card'
    TAX_ID = 'tax_id'
    RESIDENCE_CERT = 'residence_cert'
    MARRIAGE_CERT = 'marriage_cert'
    DEATH_CERT = 'death_cert'
    PASSPORT = 'passport'
    DRIVER_LICENSE = 'driver_license'
    OTHER = 'other'

@dataclass
class Document:
    """Entidade de domínio Document — NÃO é um modelo ORM.

    A infraestrutura (ORM) deve expor um modelo separado. Esta classe
    mantém apenas os dados e lógica de domínio para evitar dupla
    inscrição de tabelas no MetaData do SQLAlchemy durante import.
    """
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    citizen_id: uuid.UUID | None = None
    service_id: uuid.UUID | None = None
    document_type: str | DocumentType = DocumentType.OTHER.value
    status: str | DocumentStatus = DocumentStatus.PENDING.value
    document_number: Optional[str] = None
    request_date: datetime = field(default_factory=datetime.utcnow)
    processing_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)