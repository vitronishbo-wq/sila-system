from .generic_payment_provider_adapter import GenericPaymentProviderAdapter
from .multicaixa_real_provider import (
    MulticaixaRealProvider,
    create_multicaixa_provider,
)


def get_sqlalchemy_repository():
    from .sqlalchemy_payment_repository import SQLAlchemyPaymentRepository
    return SQLAlchemyPaymentRepository


__all__ = [
    "GenericPaymentProviderAdapter",
    "MulticaixaRealProvider",
    "create_multicaixa_provider",
]
