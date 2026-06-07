"""Schemas Pydantic do módulo taxpayer"""

from .audit_schema import *
from .certificate_schema import *
from .debt_schema import *
from .declaration_schema import *
from .error_schema import *
from .payment_schema import *
from .taxpayer_schema import *

__all__ = [
    "TaxpayerResponse",
    "TaxpayerCreate",
    "TaxpayerUpdate",
    "TaxpayerListResponse",
    "TaxpayerSummaryResponse",
    "DeclarationResponse",
    "DeclarationCreate",
    "DeclarationListResponse",
    "DeclarationStatusUpdate",
    "DebtResponse",
    "DebtCreate",
    "DebtListResponse",
    "DebtPaymentRequest",
    "PaymentResponse",
    "PaymentCreate",
    "PaymentListResponse",
    "PaymentReverseRequest",
    "CertificateResponse",
    "CertificateCreate",
    "CertificateListResponse",
    "CertificateDownloadResponse",
    "AuditLogResponse",
    "AuditSearchRequest",
    "AuditListResponse",
    "ErrorResponse",
    "ValidationErrorResponse",
    "ErrorDetail",
]
