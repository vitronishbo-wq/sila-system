"""Base repository interface (backward compatibility layer)"""

# Re-export from unified base module
from apps.backend.core.repositories.base import BaseRepository

__all__ = ["BaseRepository"]
