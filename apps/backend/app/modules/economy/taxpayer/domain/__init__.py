"""Domínio de Contribuintes (Domain-Driven Design)."""

from .aggregate_entities import AggregateEntity, TaxCertificate, TaxDebt, TaxDeclaration, TaxPayment
from .entities import Taxpayer, TaxpayerCertificate, TaxpayerDebt
from .enums import DeclarationStatus, PaymentStatus, TaxpayerStatus, TaxRegime, TaxType
from .events import TaxDebtCreated, TaxDeclarationFiled, TaxPaid, TaxpayerRegistered
from .value_objects import NIF, TaxAmount, TaxCertificateNumber, TaxDeclarationNumber, TaxPeriod

__all__ = [
    "Taxpayer",
    "TaxpayerCertificate",
    "TaxpayerDebt",
    "AggregateEntity",
    "TaxDeclaration",
    "TaxDebt",
    "TaxPayment",
    "TaxCertificate",
    "TaxpayerStatus",
    "TaxType",
    "DeclarationStatus",
    "PaymentStatus",
    "TaxRegime",
    "NIF",
    "TaxAmount",
    "TaxPeriod",
    "TaxDeclarationNumber",
    "TaxCertificateNumber",
    "TaxpayerRegistered",
    "TaxDeclarationFiled",
    "TaxPaid",
    "TaxDebtCreated",
]
