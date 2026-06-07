from uuid import uuid4

import pytest

from apps.backend.app.modules.society.familia.application.services.family_aggregate_service import (
    FamilyAggregateService,
)
from apps.backend.app.modules.society.familia.tests._fakes import (
    InMemoryFamilyRepository,
    InMemoryOutbox,
    NoopBus,
)


@pytest.mark.asyncio
async def test_create_aggregate_persists_data_and_events() -> None:
    repo = InMemoryFamilyRepository()
    outbox = InMemoryOutbox()
    service = FamilyAggregateService(repository=repo, outbox_repository=outbox, event_bus=NoopBus())
    result = await service.create_aggregate(
        head_citizen_id=uuid4(), initial_members=[], metadata={"bairro": "Maianga"}
    )
    assert result["code"].startswith("FAM-")
    assert len(outbox.events) >= 1
