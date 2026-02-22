from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class RegisterTaxpayerCommand:
    """Comando para registrar contribuinte"""
    nif: str
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    tax_regime: str
    registered_by: UUID
    ip_address: Optional[str] = None
