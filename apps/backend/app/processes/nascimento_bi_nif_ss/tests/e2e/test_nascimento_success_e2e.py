import pytest

from apps.backend.app.processes.nascimento_bi_nif_ss.handlers import NascimentoHandlers


class MockPublisher:
    def __init__(self):
        self.published = []

    async def publish_atomic(self, domain_event, **_kwargs):
        self.published.append(domain_event)
        return domain_event


@pytest.mark.asyncio
async def test_nascimento_success_e2e():
    publisher = MockPublisher()
    handlers = NascimentoHandlers(publisher)

    registro_id = await handlers.register_birth({"nome": "Test", "data": "2026-01-01"})
    await handlers.issue_certidao(registro_id, valid=True, referencia="C-123")
    await handlers.assign_nif(registro_id, "123456789")
    await handlers.assign_ss(registro_id, "SS-0001")

    event_types = [getattr(e, "event_type", None) for e in publisher.published]
    assert any("SSAtribuidoEvent" == t for t in event_types), "SS assignment event missing"
    # correlation_id must be present and equal to aggregate id for the first event
    first = publisher.published[0]
    assert getattr(first, "correlation_id", None) is not None
