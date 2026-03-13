from abc import ABC, abstractmethod
from typing import Any, Optional

class BIRepositoryPort(ABC):

    @abstractmethod
    async def get_active_by_citizen(self, citizen_fuc_id: str) -> Optional[Any]:
        pass