"""Value Objects do Domínio de Contribuintes."""

from .nif import NIF
from .tax_amount import TaxAmount
from .tax_certificate_number import TaxCertificateNumber
from .tax_declaration_number import TaxDeclarationNumber
from .tax_period import TaxPeriod

__all__ = ["NIF", "TaxAmount", "TaxPeriod", "TaxDeclarationNumber", "TaxCertificateNumber"]
