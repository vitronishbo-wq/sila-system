"""Domain Events do Domínio de Contribuintes."""
from .taxpayer_registered import TaxpayerRegistered
from .tax_declaration_filed import TaxDeclarationFiled
from .tax_paid import TaxPaid
from .tax_debt_created import TaxDebtCreated
__all__ = ['TaxpayerRegistered', 'TaxDeclarationFiled', 'TaxPaid', 'TaxDebtCreated']