"""Domain repository interfaces for Society module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
ISocietyRepository = RepositoryFactory.create_repository_interface("Society")
__all__ = ["ISocietyRepository"]
