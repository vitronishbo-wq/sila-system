"""Domain repository interfaces for Wallet module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IWalletRepository = RepositoryFactory.create_repository_interface("Wallet")
__all__ = ["IWalletRepository"]
