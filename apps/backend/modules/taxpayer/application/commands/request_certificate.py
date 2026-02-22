from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class RequestCertificateCommand:
    """Comando para solicitar certidão"""
    taxpayer_id: UUID
    certificate_type: str
    year: Optional[int]
    requested_by: UUID
    purpose: Optional[str] = None
    ip_address: Optional[str] = None
