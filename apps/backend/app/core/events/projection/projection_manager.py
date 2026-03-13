from __future__ import annotations
from collections import defaultdict
from typing import Any

class ProjectionManager:
    projections: dict[str, list] = defaultdict(list)

    @classmethod
    def register(cls, event_name: str, projection) -> None:
        cls.projections[event_name].append(projection)

    @classmethod
    async def apply(cls, event: Any) -> None:
        if isinstance(event, dict):
            event_name = event.get('name') or event.get('event_name')
        else:
            event_name = getattr(event, 'name', None) or getattr(event, 'event_name', None)
        if not event_name or event_name not in cls.projections:
            return
        for projection in cls.projections[event_name]:
            await projection.project(event)