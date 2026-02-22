from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class GetTaxCertificateQuery:
    """Query para buscar certidões"""
    taxpayer_id: UUID
    certificate_type: Optional[str] = None
    skip: int = 0
    limit: int = 100
