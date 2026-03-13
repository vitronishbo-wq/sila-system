from __future__ import annotations
from app.core.events.cqrs.registry import CQRSRegistry

class QueryBus:

    async def execute(self, query):
        handler = CQRSRegistry.queries.get(type(query))
        if not handler:
            raise Exception('Query handler not registered')
        return await handler.handle(query)