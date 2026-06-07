"""Domain repository interfaces for Audit module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IAuditRepository = RepositoryFactory.create_repository_interface("Audit")
__all__ = ["IAuditRepository"]
