from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

from ..enums.taxpayer_status import TaxpayerStatus


@dataclass
class Taxpayer:
    id: UUID = field(default_factory=uuid4)
    tenant_id: UUID = field(default_factory=uuid4)
    citizen_id: UUID = field(default_factory=uuid4)
    nif: str = ""
    name: str = ""
    status: TaxpayerStatus = TaxpayerStatus.DRAFT
    addresses: List[str] = field(default_factory=list)
    phones: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    version: int = 1

    def activate(self) -> None:
        self.status = TaxpayerStatus.ACTIVE

    def suspend(self) -> None:
        self.status = TaxpayerStatus.SUSPENDED

    def update_data(self, name: str | None = None, nif: str | None = None) -> None:
        if name:
            self.name = name
        if nif:
            self.nif = nif
        self.version += 1
        self.updated_at = datetime.utcnow()
