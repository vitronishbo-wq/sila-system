from __future__ import annotations
import asyncio
from uuid import uuid4
from apps.backend.app.modules.society.desporto.application.events import JogoAgendadoEvent
from apps.backend.app.modules.society.desporto.tests._fakes import FakeEventBus, InMemoryOutboxRepository
from apps.backend.app.modules.society.desporto.workers.estatistica_worker import EstatisticaWorker
from apps.backend.app.modules.society.desporto.workers.notificacao_worker import NotificacaoWorker
from apps.backend.app.modules.society.desporto.workers.outbox_worker import OutboxWorker
from apps.backend.app.modules.society.desporto.workers.ranking_worker import RankingWorker

def test_outbox_worker_processa_lote() -> None:

    async def scenario() -> None:
        outbox = InMemoryOutboxRepository()
        bus = FakeEventBus()
        worker = OutboxWorker(outbox_repo=outbox, event_bus=bus, batch_size=10)
        await outbox.append(JogoAgendadoEvent(jogo_id=uuid4(), codigo_jogo='JOG/2026/00001'))
        await outbox.append(JogoAgendadoEvent(jogo_id=uuid4(), codigo_jogo='JOG/2026/00002'))
        processed = await worker.process_once()
        assert processed == 2
        assert len(bus.events) == 2
        assert worker.stats['processed'] == 2
    asyncio.run(scenario())

def test_ranking_worker_process_once() -> None:

    async def scenario() -> None:
        calls = {'count': 0}

        async def _recalculate() -> int:
            calls['count'] += 1
            return 7
        worker = RankingWorker(recalculate_fn=_recalculate, interval_seconds=0.01)
        updated = await worker.process_once()
        assert updated == 7
        assert calls['count'] == 1
        assert worker.stats['runs'] == 1
        assert worker.stats['updated_items'] == 7
    asyncio.run(scenario())

def test_estatistica_e_notificacao_workers() -> None:

    async def scenario() -> None:
        stats_worker = EstatisticaWorker(collect_fn=lambda: 5, interval_seconds=0.01)
        processed = await stats_worker.process_once()
        assert processed == 5
        assert stats_worker.stats['processed_items'] == 5
        sent: list[object] = []

        async def _dispatch(item: object) -> None:
            sent.append(item)
        notif_worker = NotificacaoWorker(dispatch_fn=_dispatch, source_fn=lambda batch: [{'id': 1}, {'id': 2}][:batch], interval_seconds=0.01, batch_size=10)
        total = await notif_worker.process_once()
        assert total == 2
        assert notif_worker.stats['sent'] == 2
        assert len(sent) == 2
    asyncio.run(scenario())