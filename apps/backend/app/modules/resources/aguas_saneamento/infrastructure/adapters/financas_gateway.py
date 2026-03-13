from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.application.events.registry import AguasEventRegistry
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.financas_gateway_port import FinancasGatewayPort
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.adapters.message_publishers import BrokerPublisherFactory, MessagePublisherPort
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.resilience.circuit import circuit_breaker

class FinancasGateway(FinancasGatewayPort):
    """Gateway de integracao cross-context para o modulo de financas."""

    def __init__(self, *, publisher: MessagePublisherPort | None=None) -> None:
        self._publisher = publisher or BrokerPublisherFactory.from_env()

    @circuit_breaker('financas_gateway')
    async def registrar_fatura_agua(self, *, fatura_id: UUID, numero_fatura: str, titular_id: UUID, referencia: str, valor_total: Decimal, data_emissao: date, data_vencimento: date) -> str:
        topic = AguasEventRegistry.PUBLISHABLE_EVENTS['FaturaEmitida']
        payload = {'fatura_id': str(fatura_id), 'numero_fatura': numero_fatura, 'titular_id': str(titular_id), 'referencia': referencia, 'valor_total': str(valor_total), 'data_emissao': data_emissao.isoformat(), 'data_vencimento': data_vencimento.isoformat()}
        headers = {'source': 'aguas_saneamento', 'target_context': 'financas', 'event': 'FaturaEmitida'}
        return await self._publisher.publish(topic=topic, payload=payload, headers=headers, key=str(fatura_id))

    @circuit_breaker('financas_gateway')
    async def registrar_pagamento_fatura_agua(self, *, fatura_id: UUID, numero_fatura: str, titular_id: UUID, valor_pago: Decimal, data_pagamento: date, metodo_pagamento: str) -> str:
        topic = AguasEventRegistry.PUBLISHABLE_EVENTS['FaturaPagamentoRegistrado']
        payload = {'fatura_id': str(fatura_id), 'numero_fatura': numero_fatura, 'titular_id': str(titular_id), 'valor_pago': str(valor_pago), 'data_pagamento': data_pagamento.isoformat(), 'metodo_pagamento': metodo_pagamento}
        headers = {'source': 'aguas_saneamento', 'target_context': 'financas', 'event': 'FaturaPagamentoRegistrado'}
        return await self._publisher.publish(topic=topic, payload=payload, headers=headers, key=str(fatura_id))