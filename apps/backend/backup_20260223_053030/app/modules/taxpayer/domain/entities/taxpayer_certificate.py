from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from typing import Optional


@dataclass
class TaxpayerCertificate:
    id: UUID = field(default_factory=uuid4)
    taxpayer_id: UUID = field(default_factory=uuid4)
    certificate_type: str = "regular"
    issued_at: Optional[date] = None
    expires_at: Optional[date] = None
    reference: Optional[str] = None
