"""Modelos de domínio puros para o módulo financeiro.

Todos os modelos seguem DDD (Domain-Driven Design) com:
- Identidade única
- Regras de negócio encapsuladas
- Sem dependência de infraestrutura (ORM)
"""

from .audit_log import FinancialAudit
from .enums import CostCenterCode, InvoiceStatus, PaymentMethod, PaymentStatus, RevenueCode
from .invoice import Invoice
from .payment import Payment

__all__ = [
    "Invoice",
    "Payment",
    "FinancialAudit",
    "InvoiceStatus",
    "PaymentStatus",
    "PaymentMethod",
    "RevenueCode",
    "CostCenterCode",
]
