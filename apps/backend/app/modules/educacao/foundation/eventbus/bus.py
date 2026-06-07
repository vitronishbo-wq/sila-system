from __future__ import annotations

from typing import Any, Protocol


class EventBusPort(Protocol):
    def publish(self, topic: str, event: dict[str, Any]) -> None: ...


class BaseEventBus:
    """Light wrapper to make concrete buses consistent for tests and usage."""

    def publish(self, topic: str, event: dict[str, Any]) -> None:
        raise NotImplementedError()
