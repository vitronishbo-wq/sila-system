from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .saga_state import SagaState


class Saga(ABC):
    @abstractmethod
    async def handle(self, event: Any, state: SagaState | None = None) -> None:
        raise NotImplementedError
