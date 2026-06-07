"""Domain repository interfaces for Identity module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IIdentityRepository = RepositoryFactory.create_repository_interface("Identity")
__all__ = ["IIdentityRepository"]
