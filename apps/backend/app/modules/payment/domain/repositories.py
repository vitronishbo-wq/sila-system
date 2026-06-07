"""Domain repository interfaces for Payment module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IPaymentRepository = RepositoryFactory.create_repository_interface("Payment")
__all__ = ["IPaymentRepository"]
