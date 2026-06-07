"""Domain repository interfaces for Industry module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IIndustryRepository = RepositoryFactory.create_repository_interface("Industry")
__all__ = ["IIndustryRepository"]
