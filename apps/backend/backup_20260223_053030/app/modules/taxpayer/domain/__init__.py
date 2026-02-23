"""Domínio de Contribuintes (Domain-Driven Design)."""

from .entities import Taxpayer, TaxpayerCertificate, TaxpayerDebt
from .aggregate_entities import (
    AggregateEntity,
    TaxDeclaration,
    TaxDebt,
    TaxPayment,
    TaxCertificate,
)
from .enums import TaxpayerStatus, TaxType, DeclarationStatus, PaymentStatus, TaxRegime
from .value_objects import (
    NIF,
    TaxAmount,
    TaxPeriod,
    TaxDeclarationNumber,
    TaxCertificateNumber,
)
from .events import (
    TaxpayerRegistered,
    TaxDeclarationFiled,
    TaxPaid,
    TaxDebtCreated,
)

__all__ = [
    # Aggregate Root
    "Taxpayer",
    # Legacy Entities (será refatorado)
    "TaxpayerCertificate",
    "TaxpayerDebt",
    # Entities inside Aggregate
    "AggregateEntity",
    "TaxDeclaration",
    "TaxDebt",
    "TaxPayment",
    "TaxCertificate",
    # Enums
    "TaxpayerStatus",
    "TaxType",
    "DeclarationStatus",
    "PaymentStatus",
    "TaxRegime",
    # Value Objects
    "NIF",
    "TaxAmount",
    "TaxPeriod",
    "TaxDeclarationNumber",
    "TaxCertificateNumber",
    # Events
    "TaxpayerRegistered",
    "TaxDeclarationFiled",
    "TaxPaid",
    "TaxDebtCreated",
]
