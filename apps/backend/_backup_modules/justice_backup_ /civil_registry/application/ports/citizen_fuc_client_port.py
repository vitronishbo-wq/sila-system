from abc import ABC, abstractmethod
from typing import Any, Optional

class CitizenFUCClientPort(ABC):

    @abstractmethod
    async def get_citizen_by_id(self, citizen_fuc_id: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def validate_eligibility(self, citizen_fuc_id: str, service_code: str) -> bool:
        pass