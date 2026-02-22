from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetPaymentHistoryQuery:
    """Query para buscar histórico de pagamentos"""
    taxpayer_id: UUID
    skip: int = 0
    limit: int = 100
