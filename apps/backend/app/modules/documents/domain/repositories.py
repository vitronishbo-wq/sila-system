"""Domain repository interfaces for Documents module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IDocumentsRepository = RepositoryFactory.create_repository_interface("Documents")
__all__ = ["IDocumentsRepository"]
