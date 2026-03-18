"""Domain repository interfaces for Payment module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IPaymentRepository = RepositoryFactory.create_repository_interface('Payment')
__all__ = ['IPaymentRepository']