"""Infrastructure adapters (implements ports)"""

from .sqlalchemy_invoice_repository import SQLAlchemyInvoiceRepository
from .sqlalchemy_payment_repository import SQLAlchemyPaymentRepository


class RepositoryAdapter:
    """Adapter implementing repository port"""

    pass


class ServiceAdapter:
    """Adapter for external service calls"""

    pass


__all__ = [
    "RepositoryAdapter",
    "ServiceAdapter",
    "SQLAlchemyPaymentRepository",
    "SQLAlchemyInvoiceRepository",
]
