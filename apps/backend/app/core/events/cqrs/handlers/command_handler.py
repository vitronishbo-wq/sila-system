from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class CommandHandler(ABC):

    @abstractmethod
    async def handle(self, command: Any):
        raise NotImplementedError