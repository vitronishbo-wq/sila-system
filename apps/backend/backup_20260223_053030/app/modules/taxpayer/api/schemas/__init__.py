"""Schemas Pydantic do módulo taxpayer"""

from .taxpayer_schema import *
from .declaration_schema import *
from .debt_schema import *
from .payment_schema import *
from .certificate_schema import *
from .audit_schema import *
from .error_schema import *

__all__ = [
    # Taxpayer
    "TaxpayerResponse",
    "TaxpayerCreate",
    "TaxpayerUpdate",
    "TaxpayerListResponse",
    "TaxpayerSummaryResponse",
    
    # Declaration
    "DeclarationResponse",
    "DeclarationCreate",
    "DeclarationListResponse",
    "DeclarationStatusUpdate",
    
    # Debt
    "DebtResponse",
    "DebtCreate",
    "DebtListResponse",
    "DebtPaymentRequest",
    
    # Payment
    "PaymentResponse",
    "PaymentCreate",
    "PaymentListResponse",
    "PaymentReverseRequest",
    
    # Certificate
    "CertificateResponse",
    "CertificateCreate",
    "CertificateListResponse",
    "CertificateDownloadResponse",
    
    # Audit
    "AuditLogResponse",
    "AuditSearchRequest",
    "AuditListResponse",
    
    # Error
    "ErrorResponse",
    "ValidationErrorResponse",
    "ErrorDetail"
]
