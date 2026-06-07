from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class TaxpayerCertificate:
    id: UUID = field(default_factory=uuid4)
    taxpayer_id: UUID = field(default_factory=uuid4)
    certificate_type: str = "regular"
    issued_at: date | None = None
    expires_at: date | None = None
    reference: str | None = None
