from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Velocidade:
    download_mbps: Decimal
    upload_mbps: Decimal
    latencia_ms: Decimal

    def is_conforme(
        self, *, download_min: Decimal, upload_min: Decimal, latencia_max: Decimal
    ) -> bool:
        return (
            self.download_mbps >= download_min
            and self.upload_mbps >= upload_min
            and (self.latencia_ms <= latencia_max)
        )
