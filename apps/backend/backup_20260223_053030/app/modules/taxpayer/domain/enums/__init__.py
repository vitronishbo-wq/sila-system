"""Enums do Domínio de Contribuintes."""

from .taxpayer_status import TaxpayerStatus
from .tax_type import TaxType
from .declaration_status import DeclarationStatus
from .payment_status import PaymentStatus
from .tax_regime import TaxRegime

__all__ = [
    "TaxpayerStatus",
    "TaxType",
    "DeclarationStatus",
    "PaymentStatus",
    "TaxRegime",
]
