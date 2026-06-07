"""Core repositories module - shared across all domains"""

from .base_repository import BaseRepository
from .repository_factory import RepositoryFactory

__all__ = [
    "BaseRepository",
    "RepositoryFactory",
]
