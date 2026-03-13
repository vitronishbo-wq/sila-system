from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import uuid4
import pytest
from app.modules.resources.aguas_saneamento.infrastructure.adapters.financas_gateway import FinancasGateway

class _FakePublisher:

    def __init__(self) -> None:
        self.calls: list[dict] = []

    async def publish(self, *, topic, payload, headers=None, key=None) -> str:
        self.calls.append({'topic': topic, 'payload': payload, 'headers': headers or {}, 'key': key})
        return 'MSG-123'

@pytest.mark.asyncio
async def test_financas_gateway_publica_evento_fatura_emitida():
    fake = _FakePublisher()
    gateway = FinancasGateway(publisher=fake)
    result = await gateway.registrar_fatura_agua(fatura_id=uuid4(), numero_fatura='FAT/2026/000001', titular_id=uuid4(), referencia='2026-03', valor_total=Decimal('250.00'), data_emissao=date(2026, 3, 4), data_vencimento=date(2026, 3, 14))
    assert result == 'MSG-123'
    assert len(fake.calls) == 1
    assert fake.calls[0]['topic'] == 'aguas.fatura.emitida'
    assert fake.calls[0]['payload']['numero_fatura'] == 'FAT/2026/000001'

@pytest.mark.asyncio
async def test_financas_gateway_publica_evento_pagamento():
    fake = _FakePublisher()
    gateway = FinancasGateway(publisher=fake)
    result = await gateway.registrar_pagamento_fatura_agua(fatura_id=uuid4(), numero_fatura='FAT/2026/000001', titular_id=uuid4(), valor_pago=Decimal('250.00'), data_pagamento=date(2026, 3, 5), metodo_pagamento='multicaixa')
    assert result == 'MSG-123'
    assert len(fake.calls) == 1
    assert fake.calls[0]['topic'] == 'aguas.fatura.pagamento_registrado'
    assert fake.calls[0]['payload']['metodo_pagamento'] == 'multicaixa'