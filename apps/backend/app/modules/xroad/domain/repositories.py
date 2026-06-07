"""Domain repository interfaces for XRoad module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IXRoadRepository = RepositoryFactory.create_repository_interface("XRoad")
__all__ = ["IXRoadRepository"]
