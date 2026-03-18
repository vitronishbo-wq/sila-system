import os
from uuid import uuid4
import pytest
from sqlalchemy import select
from apps.backend.app.core.events.outbox.outbox_model import OutboxEvent
from apps.backend.app.modules.justice._deprecated.bounded_contexts.vital_events.application.services.birth_service import BirthService
from apps.backend.app.modules.justice._deprecated.bounded_contexts.vital_events.infrastructure.repositories.birth_repository import BirthRepository
from apps.backend.app.modules.justice._deprecated.bounded_contexts.civil_registry_core.infrastructure.repositories.citizen_repository import CitizenRepository

class _StubFUC:

    async def create_or_link(self, data):
        return uuid4()

@pytest.mark.asyncio
@pytest.mark.skipif(os.getenv('RUN_DB_INTEGRATION') != '1', reason='Requires seeded Postgres dataset. Set RUN_DB_INTEGRATION=1 to run.')
async def test_citizen_registration_outbox(db_session):
    birth_repo = BirthRepository(db_session)
    citizen_repo = CitizenRepository(db_session)
    service = BirthService(repo=birth_repo, fuc=_StubFUC(), citizen_repo=citizen_repo, db_session=db_session)
    data = {'nub': 'NUB-TEST-001', 'full_name': 'Test Citizen', 'date_of_birth': '2025-01-01', 'place_of_birth': 'Luanda', 'bi_number': '000123456LA042', 'request_id': 'req-test'}
    await service.register_birth(data, data['bi_number'], request_id=data['request_id'])
    result = await db_session.execute(select(OutboxEvent).order_by(OutboxEvent.created_at.desc()).limit(1))
    assert result.scalars().first() is not None