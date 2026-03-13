from __future__ import annotations
import asyncio
from datetime import datetime
from app.modules.governance.cooperacao_internacional.domain.enums import StatusAcordo, TipoAcordo

class TratadoMonitorWorker:

    def __init__(self, *, acordo_repo, mre_adapter=None, onu_adapter=None, check_interval: int=86400) -> None:
        self.acordo_repo = acordo_repo
        self.mre = mre_adapter
        self.onu = onu_adapter
        self.check_interval = check_interval
        self.running = False
        self.stats = {'acordos_verificados': 0, 'alertas_emitidos': 0, 'ultimo_check': None}

    async def start(self) -> None:
        self.running = True
        while self.running:
            await self._monitorar_tratados()
            self.stats['ultimo_check'] = datetime.utcnow().isoformat()
            await asyncio.sleep(self.check_interval)

    async def stop(self) -> None:
        self.running = False

    async def _monitorar_tratados(self) -> None:
        acordos = await self.acordo_repo.find_em_vigor()
        for acordo in acordos:
            self.stats['acordos_verificados'] += 1
            dias_restantes = acordo.vigencia_restante_dias()
            if dias_restantes is None:
                continue
            if dias_restantes <= 90:
                self.stats['alertas_emitidos'] += 1
                if self.mre is not None:
                    await self.mre.registrar_acordo({'numero': acordo.numero_registro, 'alerta': 'vencimento_proximo', 'dias_restantes': dias_restantes})
            if dias_restantes == 0:
                acordo.status = StatusAcordo.EXTINTO
                await self.acordo_repo.save(acordo)
                if self.onu is not None and acordo.tipo == TipoAcordo.TRATADO:
                    await self.onu.registrar_extincao(numero_acordo=acordo.numero_registro, data_extincao=datetime.utcnow().date())