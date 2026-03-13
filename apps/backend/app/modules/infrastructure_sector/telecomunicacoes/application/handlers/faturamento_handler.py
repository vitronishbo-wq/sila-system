from __future__ import annotations
from app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import FaturaTelecomGeradaEvent

class FaturamentoHandler:

    def __init__(self) -> None:
        self.last_invoice_event: FaturaTelecomGeradaEvent | None = None

    async def on_fatura_gerada(self, event: FaturaTelecomGeradaEvent) -> None:
        self.last_invoice_event = event