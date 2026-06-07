"""Domain repository interfaces for Infrastructure module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IInfrastructureRepository = RepositoryFactory.create_repository_interface("Infrastructure")
__all__ = ["IInfrastructureRepository"]
