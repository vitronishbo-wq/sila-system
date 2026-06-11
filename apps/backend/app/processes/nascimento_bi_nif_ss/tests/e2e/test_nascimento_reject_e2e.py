import pytest

from apps.backend.app.processes.nascimento_bi_nif_ss.handlers import NascimentoHandlers


class MockPublisher:
    def __init__(self):
        self.published = []

    async def publish_atomic(self, domain_event, **_kwargs):
        self.published.append(domain_event)
        return domain_event


@pytest.mark.asyncio
async def test_nascimento_reject_e2e():
    publisher = MockPublisher()
    handlers = NascimentoHandlers(publisher)

    registro_id = await handlers.register_birth({"nome": "Test Rej", "data": "2026-01-01"})
    # issue certidao but mark invalid (rejected)
    await handlers.issue_certidao(registro_id, valid=False, referencia="C-REJ")

    event_types = [getattr(e, "event_type", None) for e in publisher.published]
    assert any("CertidaoEmitidaEvent" == t for t in event_types)
    # no NIF/SS events after rejection
    assert not any("NIFAtribuidoEvent" == t for t in event_types)
