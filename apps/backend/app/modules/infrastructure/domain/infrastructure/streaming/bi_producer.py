from __future__ import annotations
import json
import os
from typing import Any
from apps.backend.app.modules.infrastructure.infrastructure.observability.tracing import start_span
from apps.backend.app.modules.infrastructure.infrastructure.resilience.bulkhead import AsyncBulkhead
from apps.backend.app.modules.infrastructure.infrastructure.resilience.rate_limit import AsyncRateLimiter
from apps.backend.app.modules.infrastructure.infrastructure.resilience.timeout import with_timeout

class BIProducer:

    def __init__(self) -> None:
        self._bootstrap_servers = os.environ.get('OP_BI_KAFKA_BOOTSTRAP_SERVERS', '').strip()
        self._enabled = os.environ.get('OP_ENABLE_BI_STREAMING', '1') == '1'
        self._timeout_seconds = float(os.environ.get('OP_BI_TIMEOUT_SECONDS', '5'))
        self._bulkhead = AsyncBulkhead(limit=int(os.environ.get('OP_BI_BULKHEAD_LIMIT', '20')))
        self._rate_limiter = AsyncRateLimiter(rate=int(os.environ.get('OP_BI_RATE_LIMIT', '500')), per_seconds=60.0)

    async def publish(self, *, topic: str, payload: dict[str, Any]) -> None:
        if not self._enabled:
            return
        if not self._bootstrap_servers:
            return
        try:
            from aiokafka import AIOKafkaProducer
        except Exception:
            return
        await self._rate_limiter.acquire()
        async with self._bulkhead:
            with start_span('obras_publicas.bi_stream.publish', {'topic': topic}):
                producer = AIOKafkaProducer(bootstrap_servers=self._bootstrap_servers)
                await with_timeout(producer.start(), timeout_seconds=self._timeout_seconds)
                try:
                    await with_timeout(producer.send_and_wait(topic, json.dumps(payload).encode('utf-8')), timeout_seconds=self._timeout_seconds)
                finally:
                    await with_timeout(producer.stop(), timeout_seconds=self._timeout_seconds)
