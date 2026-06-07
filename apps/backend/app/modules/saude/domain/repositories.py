"""Domain repository interfaces for Saude module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
ISaudeRepository = RepositoryFactory.create_repository_interface("Saude")
__all__ = ["ISaudeRepository"]
