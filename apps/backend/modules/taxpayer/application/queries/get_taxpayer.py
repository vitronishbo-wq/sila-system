from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class GetTaxpayerQuery:
    """Query para buscar contribuinte"""
    taxpayer_id: Optional[UUID] = None
    nif: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
