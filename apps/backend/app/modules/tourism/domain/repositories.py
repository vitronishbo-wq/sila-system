"""Domain repository interfaces for Tourism module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
ITourismRepository = RepositoryFactory.create_repository_interface("Tourism")
__all__ = ["ITourismRepository"]
