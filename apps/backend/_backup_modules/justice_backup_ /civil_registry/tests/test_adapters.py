import pytest
from uuid import uuid4
from apps.backend.app.modules.justice.bounded_contexts.application.services.service import CitizenService
from apps.backend.app.modules.justice.bounded_contexts.enums import CitizenStatus

class MockFUCAdapter:

    async def get_citizen(self, citizen_id):
        return {'id': str(citizen_id), 'full_name': 'Mock User', 'status': CitizenStatus.ACTIVE, 'document_type': 'BI'}

@pytest.mark.asyncio
async def test_citizen_service_uses_fuc_adapter():
    mock_adapter = MockFUCAdapter()
    service = CitizenService(db_session=None, fuc_adapter=mock_adapter)
    cid = str(uuid4())
    data = await service.get_citizen_data(cid)
    assert data['full_name'] == 'Mock User'
    valid = await service.validate_citizen(cid)
    assert valid is True