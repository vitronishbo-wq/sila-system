"""Domain repository interfaces for Resources module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IResourcesRepository = RepositoryFactory.create_repository_interface("Resources")
__all__ = ["IResourcesRepository"]
