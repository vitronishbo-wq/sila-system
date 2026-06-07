"""Domain repository interfaces for Economy module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IEconomyRepository = RepositoryFactory.create_repository_interface("Economy")
__all__ = ["IEconomyRepository"]
