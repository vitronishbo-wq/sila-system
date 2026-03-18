"""
Infrastructure adapters for audit module.
"""
from abc import ABC, abstractmethod
from typing import Any, List

class AuditPort(ABC):
    """Port (interface) for audit operations."""

    @abstractmethod
    async def get(self, id: str) -> Any:
        """Get audit by ID."""
        pass

    @abstractmethod
    async def create(self, data: dict) -> Any:
        """Create new audit."""
        pass

    @abstractmethod
    async def update(self, id: str, data: dict) -> Any:
        """Update audit."""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete audit."""
        pass

    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all audit."""
        pass

class AuditAdapter(AuditPort):
    """Adapter (implementation) for audit operations."""

    async def get(self, id: str) -> Any:
        """Get audit by ID."""
        return None

    async def create(self, data: dict) -> Any:
        """Create new audit."""
        return {'id': id, **data}

    async def update(self, id: str, data: dict) -> Any:
        """Update audit."""
        return {'id': id, **data}

    async def delete(self, id: str) -> bool:
        """Delete audit."""
        return True

    async def list_all(self) -> List[Any]:
        """List all audit."""
        return []