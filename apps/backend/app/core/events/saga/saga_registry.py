from __future__ import annotations
from typing import List
from .saga import Saga

class SagaRegistry:
    sagas: List[Saga] = []

    @classmethod
    def register(cls, saga: Saga) -> None:
        cls.sagas.append(saga)

    @classmethod
    def get_sagas(cls) -> List[Saga]:
        return cls.sagas