"""Domain repository interfaces for Logistics module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
ILogisticsRepository = RepositoryFactory.create_repository_interface("Logistics")
__all__ = ["ILogisticsRepository"]
