import pytest
from app.modules.society.familia.application.services.family_projection_handler import FamilyProjectionHandler

class _ProjectionRepo:

    def __init__(self) -> None:
        self.payload = None

    async def upsert_family_composition(self, payload: dict) -> None:
        self.payload = payload

class _FamilyRepo:

    async def get_by_id(self, family_id):
        _ = family_id
        return None

@pytest.mark.asyncio
async def test_projection_handler_upserts_payload() -> None:
    repo = _ProjectionRepo()
    handler = FamilyProjectionHandler(projection_repository=repo, family_repository=_FamilyRepo())
    payload = {'family_id': 'abc', 'member_count': 3}
    await handler.on_family_changed(payload)
    assert repo.payload == payload