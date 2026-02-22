"""Query handlers para consultas CQRS"""

from .get_taxpayer import GetTaxpayerQuery
from .get_declaration_history import GetDeclarationHistoryQuery
from .get_tax_debt import GetTaxDebtQuery
from .get_payment_history import GetPaymentHistoryQuery
from .get_tax_certificate import GetTaxCertificateQuery

__all__ = [
    "GetTaxpayerQuery",
    "GetDeclarationHistoryQuery",
    "GetTaxDebtQuery",
    "GetPaymentHistoryQuery",
    "GetTaxCertificateQuery"
]
