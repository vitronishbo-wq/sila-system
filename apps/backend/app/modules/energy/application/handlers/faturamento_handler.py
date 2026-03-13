from __future__ import annotations
from apps.backend.app.modules.energy.application.events.definitions import LeituraRealizadaEvent
from apps.backend.app.modules.energy.application.services.faturamento_service import FaturamentoService
from apps.backend.app.modules.energy.domain.exceptions import FaturaEnergiaAlreadyExistsError

class FaturamentoHandler:

    def __init__(self, *, faturamento_service: FaturamentoService) -> None:
        self._faturamento_service = faturamento_service

    async def on_leitura_realizada(self, event: LeituraRealizadaEvent) -> None:
        if event.data_leitura.day < 25:
            return
        try:
            await self._faturamento_service.gerar_fatura_por_consumo(event.consumo_id, data_referencia=event.data_leitura.date())
        except FaturaEnergiaAlreadyExistsError:
            return
