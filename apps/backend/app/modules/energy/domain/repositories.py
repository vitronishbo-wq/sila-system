"""Domain repository interfaces for Energy module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IEnergyRepository = RepositoryFactory.create_repository_interface("Energy")
__all__ = ["IEnergyRepository"]
