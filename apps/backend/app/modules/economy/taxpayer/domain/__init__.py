"""Domínio de Contribuintes (Domain-Driven Design)."""
from .entities import Taxpayer, TaxpayerCertificate, TaxpayerDebt
from .aggregate_entities import AggregateEntity, TaxDeclaration, TaxDebt, TaxPayment, TaxCertificate
from .enums import TaxpayerStatus, TaxType, DeclarationStatus, PaymentStatus, TaxRegime
from .value_objects import NIF, TaxAmount, TaxPeriod, TaxDeclarationNumber, TaxCertificateNumber
from .events import TaxpayerRegistered, TaxDeclarationFiled, TaxPaid, TaxDebtCreated
__all__ = ['Taxpayer', 'TaxpayerCertificate', 'TaxpayerDebt', 'AggregateEntity', 'TaxDeclaration', 'TaxDebt', 'TaxPayment', 'TaxCertificate', 'TaxpayerStatus', 'TaxType', 'DeclarationStatus', 'PaymentStatus', 'TaxRegime', 'NIF', 'TaxAmount', 'TaxPeriod', 'TaxDeclarationNumber', 'TaxCertificateNumber', 'TaxpayerRegistered', 'TaxDeclarationFiled', 'TaxPaid', 'TaxDebtCreated']