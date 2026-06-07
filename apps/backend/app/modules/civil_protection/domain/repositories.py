"""Domain repository interfaces for CivilProtection module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
ICivilProtectionRepository = RepositoryFactory.create_repository_interface("CivilProtection")
__all__ = ["ICivilProtectionRepository"]
