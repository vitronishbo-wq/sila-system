from __future__ import annotations
from apps.backend.app.modules.energy.application.events.definitions import FaturaGeradaEvent, QualidadeInconformeEvent
from apps.backend.app.modules.energy.infrastructure.adapters.aneel_adapter import ANEELAdapter

class AuditoriaHandler:

    def __init__(self, *, aneel_adapter: ANEELAdapter | None=None) -> None:
        self._aneel_adapter = aneel_adapter

    async def on_fatura_gerada(self, event: FaturaGeradaEvent) -> None:
        if self._aneel_adapter is None:
            return
        await self._aneel_adapter.registrar_evento_qualidade({'tipo_evento': 'fatura_gerada', 'fatura_id': str(event.fatura_id), 'numero_fatura': event.numero_fatura, 'valor_total': str(event.valor_total), 'mes_referencia': event.mes_referencia})

    async def on_qualidade_inconforme(self, event: QualidadeInconformeEvent) -> None:
        if self._aneel_adapter is None:
            return
        await self._aneel_adapter.registrar_evento_qualidade({'tipo_evento': 'qualidade_inconforme', 'ponto_medicao_id': str(event.ponto_medicao_id), 'parametro': event.parametro, 'valor_medido': str(event.valor_medido), 'valor_referencia': str(event.valor_referencia), 'desvio_percentual': str(event.desvio_percentual)})
