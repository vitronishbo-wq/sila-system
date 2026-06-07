from abc import ABC, abstractmethod


class RequestServicePort(ABC):
    @abstractmethod
    async def available(self) -> bool:
        pass
