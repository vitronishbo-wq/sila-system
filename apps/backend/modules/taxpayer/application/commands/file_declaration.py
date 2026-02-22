from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class FileDeclarationCommand:
    """Comando para submeter declaração"""
    taxpayer_id: UUID
    tax_type: str
    tax_period: str
    gross_amount: float
    deductions: Optional[float]
    submitted_by: UUID
    ip_address: Optional[str] = None
