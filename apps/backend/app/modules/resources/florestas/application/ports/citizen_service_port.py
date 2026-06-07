from abc import ABC, abstractmethod


class CitizenServicePort(ABC):
    @abstractmethod
    async def available(self) -> bool:
        pass
