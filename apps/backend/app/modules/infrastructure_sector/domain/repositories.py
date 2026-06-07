"""Domain repository interfaces for InfrastructureSector module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IInfrastructureSectorRepository = RepositoryFactory.create_repository_interface(
    "InfrastructureSector"
)
__all__ = ["IInfrastructureSectorRepository"]
