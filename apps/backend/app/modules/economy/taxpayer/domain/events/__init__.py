"""Domain Events do Domínio de Contribuintes."""

from .tax_debt_created import TaxDebtCreated
from .tax_declaration_filed import TaxDeclarationFiled
from .tax_paid import TaxPaid
from .taxpayer_registered import TaxpayerRegistered

__all__ = ["TaxpayerRegistered", "TaxDeclarationFiled", "TaxPaid", "TaxDebtCreated"]
