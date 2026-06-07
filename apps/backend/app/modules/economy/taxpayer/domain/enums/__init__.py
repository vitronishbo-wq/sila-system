"""Enums do Domínio de Contribuintes."""

from .declaration_status import DeclarationStatus
from .payment_status import PaymentStatus
from .tax_regime import TaxRegime
from .tax_type import TaxType
from .taxpayer_status import TaxpayerStatus

__all__ = ["TaxpayerStatus", "TaxType", "DeclarationStatus", "PaymentStatus", "TaxRegime"]
