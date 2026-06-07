"""Infrastructure adapters for Payment module"""

from apps.backend.app.modules.payment.domain.repositories import IPaymentRepository
from apps.backend.core.adapters.adapter_factory import AdapterFactory

PaymentAdapter = AdapterFactory.create_infrastructure_adapter(
    module_name="Payment", repository_interface=IPaymentRepository
)
__all__ = ["PaymentAdapter"]
