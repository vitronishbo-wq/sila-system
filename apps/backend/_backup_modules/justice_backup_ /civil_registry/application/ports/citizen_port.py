from abc import ABC, abstractmethod
from typing import Optional

class CitizenPort(ABC):

    @abstractmethod
    async def get(self, citizen_id: str) -> Optional[dict]:
        """Return citizen payload or None."""

    @abstractmethod
    async def validate(self, citizen_id: str) -> bool:
        """Validate citizen existence."""