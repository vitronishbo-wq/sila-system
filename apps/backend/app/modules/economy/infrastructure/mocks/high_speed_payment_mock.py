from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class HighSpeedPaymentMock:
    ledger: list = field(default_factory=list)
    processed_count: int = 0
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)

    async def request_funds(self, request_data: dict):
        await asyncio.sleep(random.uniform(0.001, 0.005))
        async with self._lock:
            entry = {
                "id": f"tx_{self.processed_count}",
                "timestamp": datetime.now(),
                **request_data,
            }
            self.ledger.append(entry)
            self.processed_count += 1
        return {"status": "SUCCESS", "tx_id": entry["id"]}

    def get_metrics(self):
        return {"total_processed": self.processed_count, "ledger_size": len(self.ledger)}
