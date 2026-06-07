from __future__ import annotations

from apps.backend.app.core.events.cqrs.registry import CQRSRegistry


class CommandBus:
    async def execute(self, command):
        handler = CQRSRegistry.commands.get(type(command))
        if not handler:
            raise Exception("Command handler not registered")
        return await handler.handle(command)
