"""Domain repository interfaces for Governance module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IGovernanceRepository = RepositoryFactory.create_repository_interface("Governance")
__all__ = ["IGovernanceRepository"]
