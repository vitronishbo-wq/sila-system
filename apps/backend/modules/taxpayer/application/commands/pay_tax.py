from dataclasses import dataclass
from uuid import UUID
from typing import List, Optional


@dataclass
class PayTaxCommand:
    """Comando para realizar pagamento"""
    taxpayer_id: UUID
    amount: float
    payment_method: str
    paid_by: UUID
    debt_ids: Optional[List[UUID]] = None
    reference: Optional[str] = None
    metadata: Optional[dict] = None
    ip_address: Optional[str] = None
