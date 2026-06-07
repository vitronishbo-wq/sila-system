"""
Event handlers for procurement module.
"""

from collections.abc import Callable
from typing import Any


class ProcurementEventHandlers:
    """Handles all events for procurement module."""

    def __init__(self):
        self.handlers: dict[str, Callable] = {}
        self._register_handlers()

    def _register_handlers(self) -> None:
        """Register all event handlers."""
        pass

    def handle(self, event_type: str, event_data: Any) -> None:
        """Handle an event if handler exists."""
        if event_type in self.handlers:
            self.handlers[event_type](event_data)


handlers = ProcurementEventHandlers()
