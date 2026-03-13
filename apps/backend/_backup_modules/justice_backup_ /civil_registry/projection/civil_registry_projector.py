from __future__ import annotations
from typing import Any
from app.core.events.projection.base_projection import BaseProjection

class CivilRegistryProjector(BaseProjection):
    event_type = 'CITIZEN_REGISTERED'

    def __init__(self, session):
        self._session = session

    async def project(self, event: Any) -> None:
        if isinstance(event, dict):
            payload = event.get('payload', {})
            aggregate_id = event.get('aggregate_id') or payload.get('citizen_id')
        else:
            payload = getattr(event, 'payload', None) or {}
            aggregate_id = getattr(event, 'aggregate_id', None) or payload.get('citizen_id')
        if not aggregate_id:
            return
        query = '\n        INSERT INTO civil_registry_summary_view\n        (citizen_id, name, birth_date)\n        VALUES (:id, :name, :birth)\n        '
        await self._session.execute(query, {'id': aggregate_id, 'name': payload.get('name') or payload.get('full_name'), 'birth': payload.get('birth_date') or payload.get('date_of_birth')})