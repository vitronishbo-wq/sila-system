import pytest

from apps.backend.app.processes.nascimento_bi_nif_ss.handlers import NascimentoHandlers


class MockPublisher:
    def __init__(self):
        self.published = []

    async def publish_atomic(self, domain_event, **_kwargs):
        self.published.append(domain_event)
        return domain_event


@pytest.mark.asyncio
async def test_nascimento_cancel_e2e():
    publisher = MockPublisher()
    handlers = NascimentoHandlers(publisher)

    registro_id = await handlers.register_birth({"nome": "Test Cancel", "data": "2026-01-01"})
    await handlers.cancel(registro_id, motivo="user_cancelled")

    event_types = [getattr(e, "event_type", None) for e in publisher.published]
    assert any("RegistroCanceladoEvent" == t for t in event_types)
