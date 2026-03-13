from __future__ import annotations
from app.modules.resources.aguas_saneamento.application.events.fatura_events import FaturaEmitidaEvent, FaturaPagamentoRegistradoEvent
from app.modules.resources.aguas_saneamento.application.ports.financas_gateway_port import FinancasGatewayPort

class FinancasIntegrationHandler:

    def __init__(self, *, gateway: FinancasGatewayPort) -> None:
        self._gateway = gateway

    async def on_fatura_emitida(self, event: FaturaEmitidaEvent) -> None:
        await self._gateway.registrar_fatura_agua(fatura_id=event.fatura_id, numero_fatura=event.numero_fatura, titular_id=event.titular_id, referencia=event.referencia, valor_total=event.valor_total, data_emissao=event.data_emissao, data_vencimento=event.data_vencimento)

    async def on_fatura_pagamento_registrado(self, event: FaturaPagamentoRegistradoEvent) -> None:
        await self._gateway.registrar_pagamento_fatura_agua(fatura_id=event.fatura_id, numero_fatura=event.numero_fatura, titular_id=event.titular_id, valor_pago=event.valor_pago, data_pagamento=event.data_pagamento, metodo_pagamento=event.metodo_pagamento)