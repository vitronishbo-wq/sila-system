"""
Ports (Interface Contracts)
Define contratos obrigatórios para repositórios
"""
from .invoice_repository_port import InvoiceRepositoryPort
from .payment_repository_port import PaymentRepositoryPort

__all__ = ["InvoiceRepositoryPort", "PaymentRepositoryPort"]
