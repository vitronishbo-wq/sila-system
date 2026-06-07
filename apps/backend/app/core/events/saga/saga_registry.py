from __future__ import annotations

from .saga import Saga


class SagaRegistry:
    sagas: list[Saga] = []

    @classmethod
    def register(cls, saga: Saga) -> None:
        cls.sagas.append(saga)

    @classmethod
    def get_sagas(cls) -> list[Saga]:
        return cls.sagas
