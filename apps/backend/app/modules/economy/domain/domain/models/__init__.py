"""Modelos de domínio puros para o módulo financeiro.

Todos os modelos seguem DDD (Domain-Driven Design) com:
- Identidade única
- Regras de negócio encapsuladas
- Sem dependência de infraestrutura (ORM)
"""
from .invoice import Invoice
from .payment import Payment
from .audit_log import FinancialAudit
from .enums import InvoiceStatus, PaymentStatus, PaymentMethod, RevenueCode, CostCenterCode
__all__ = ['Invoice', 'Payment', 'FinancialAudit', 'InvoiceStatus', 'PaymentStatus', 'PaymentMethod', 'RevenueCode', 'CostCenterCode']