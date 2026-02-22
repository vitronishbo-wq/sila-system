from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetTaxDebtQuery:
    """Query para buscar dívidas"""
    taxpayer_id: UUID
    include_paid: bool = False
    skip: int = 0
    limit: int = 100
