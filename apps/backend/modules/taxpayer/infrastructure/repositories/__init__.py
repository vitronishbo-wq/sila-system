"""Repositories for taxpayer module"""

from .base_repository import BaseRepository
from .taxpayer_repository import TaxpayerRepository
from .declaration_repository import DeclarationRepository
from .debt_repository import DebtRepository
from .payment_repository import PaymentRepository
from .certificate_repository import CertificateRepository
from .audit_repository import AuditRepository

__all__ = [
    "BaseRepository",
    "TaxpayerRepository",
    "DeclarationRepository",
    "DebtRepository",
    "PaymentRepository",
    "CertificateRepository",
    "AuditRepository"
]
