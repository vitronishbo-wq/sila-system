from __future__ import annotations
import asyncio
import os
from app.modules.infrastructure.infrastructure.messaging.outbox_worker import OutboxWorker
try:
    from prometheus_client import start_http_server
except Exception:
    start_http_server = None

async def run() -> None:
    if start_http_server is not None:
        metrics_port = int(os.environ.get('OP_WORKER_METRICS_PORT', '9108'))
        start_http_server(metrics_port)
    worker = OutboxWorker(batch_size=int(os.environ.get('OP_OUTBOX_BATCH_SIZE', '50')), max_failed_attempts=int(os.environ.get('OP_OUTBOX_MAX_FAILED_ATTEMPTS', '15')))
    interval_seconds = float(os.environ.get('OP_OUTBOX_POLL_INTERVAL_SECONDS', '2.0'))
    await worker.run_forever(interval_seconds=interval_seconds)

def main() -> None:
    asyncio.run(run())
if __name__ == '__main__':
    main()
