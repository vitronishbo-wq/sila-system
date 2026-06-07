"""Domain repository interfaces for Intelligence module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IIntelligenceRepository = RepositoryFactory.create_repository_interface("Intelligence")
__all__ = ["IIntelligenceRepository"]
