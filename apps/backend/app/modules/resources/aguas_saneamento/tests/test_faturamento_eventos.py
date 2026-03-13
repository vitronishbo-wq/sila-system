from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, timezone
import pytest
from apps.backend.app.modules.resources.aguas_saneamento.application.bus import EventBus
from apps.backend.app.modules.resources.aguas_saneamento.application.events.registry import AguasEventRegistry, serialize_event
from apps.backend.app.modules.resources.aguas_saneamento.application.handlers.financas_integration_handler import FinancasIntegrationHandler
from apps.backend.app.modules.resources.aguas_saneamento.application.services.faturamento_service import FaturamentoService
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import MetodoPagamento
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.persistence.outbox import OutboxMessage
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.repositories import SQLAlchemyFaturaRepository
from apps.backend.app.modules.resources.aguas_saneamento.workers.outbox_worker import OutboxWorker

class _TestOutboxRepository:

    def __init__(self) -> None:
        self._items: dict = {}

    async def enqueue(self, event) -> OutboxMessage:
        event_name, payload = serialize_event(event)
        topic = AguasEventRegistry.PUBLISHABLE_EVENTS.get(event_name, event_name)
        message = OutboxMessage(id=uuid4(), event_name=event_name, topic=topic, payload=payload, headers={}, event_version=int(payload.get('version', 1)), schema_version=1, processed=False, retries=0, created_at=datetime.now(timezone.utc))
        self._items[message.id] = message
        return message

    async def get_pending(self, *, limit: int=100):
        pending = [item for item in self._items.values() if not item.processed]
        pending.sort(key=lambda item: item.created_at)
        return pending[:limit]

    async def mark_done(self, message_id):
        item = self._items.get(message_id)
        if not item:
            return
        item.processed = True
        item.processed_at = datetime.now(timezone.utc)
        item.last_error = None

    async def increment_retries(self, message_id, *, error: str | None=None):
        item = self._items.get(message_id)
        if not item:
            return
        item.retries += 1
        item.last_error = error

@pytest.mark.asyncio
async def test_emissao_publica_evento_e_worker_entrega_no_gateway():
    outbox_repo = _TestOutboxRepository()
    service = FaturamentoService(fatura_repo=SQLAlchemyFaturaRepository(), outbox_repo=outbox_repo)
    gateway = SimpleNamespace(registrar_fatura_agua=AsyncMock(return_value='FIN-AGUA-FAT-1'), registrar_pagamento_fatura_agua=AsyncMock(return_value='FIN-AGUA-PAG-1'))
    handler = FinancasIntegrationHandler(gateway=gateway)
    bus = EventBus()
    bus.subscribe('FaturaEmitida', handler.on_fatura_emitida)
    bus.subscribe('FaturaPagamentoRegistrado', handler.on_fatura_pagamento_registrado)
    worker = OutboxWorker(outbox_repo=outbox_repo, event_bus=bus)
    fatura = await service.emitir(consumo_id=uuid4(), titular_id=uuid4(), referencia='2026-03', volume_m3=Decimal('15.00'), tarifa_m3=Decimal('20.00'), data_vencimento=date.today() + timedelta(days=5))
    pendentes = await outbox_repo.get_pending()
    assert len(pendentes) == 1
    assert pendentes[0].event_name == 'FaturaEmitida'
    processados = await worker.process_once()
    assert processados == 1
    pendentes = await outbox_repo.get_pending()
    assert len(pendentes) == 0
    gateway.registrar_fatura_agua.assert_awaited_once()
    await service.registrar_pagamento(fatura.numero_fatura, data_pagamento=date.today(), valor_pago=fatura.valor_total, metodo_pagamento=MetodoPagamento.MULTICAIXA)
    pendentes = await outbox_repo.get_pending()
    assert len(pendentes) == 1
    assert pendentes[0].event_name == 'FaturaPagamentoRegistrado'
    await worker.process_once()
    gateway.registrar_pagamento_fatura_agua.assert_awaited_once()

@pytest.mark.asyncio
async def test_worker_incrementa_retry_quando_handler_falha():
    outbox_repo = _TestOutboxRepository()
    service = FaturamentoService(fatura_repo=SQLAlchemyFaturaRepository(), outbox_repo=outbox_repo)
    bus = EventBus()

    async def failing_handler(_event):
        raise RuntimeError('falha de integracao')
    bus.subscribe('FaturaEmitida', failing_handler)
    worker = OutboxWorker(outbox_repo=outbox_repo, event_bus=bus)
    await service.emitir(consumo_id=uuid4(), titular_id=uuid4(), referencia='2026-03', volume_m3=Decimal('10.00'), tarifa_m3=Decimal('22.00'), data_vencimento=date.today() + timedelta(days=5))
    pendentes = await outbox_repo.get_pending()
    assert len(pendentes) == 1
    processados = await worker.process_once()
    assert processados == 0
    pendentes = await outbox_repo.get_pending()
    assert len(pendentes) == 1
    assert pendentes[0].retries == 1