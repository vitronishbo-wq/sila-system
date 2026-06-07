"""Domain repository interfaces for Api module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IApiRepository = RepositoryFactory.create_repository_interface("Api")
__all__ = ["IApiRepository"]
