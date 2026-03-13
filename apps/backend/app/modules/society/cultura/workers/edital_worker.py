from __future__ import annotations
import asyncio
from datetime import datetime
from app.modules.society.cultura.domain.enums import FaseEditalCultural

class EditalWorker:

    def __init__(self, *, edital_repo, check_interval: int=3600) -> None:
        self.edital_repo = edital_repo
        self.check_interval = check_interval
        self.running = False
        self.stats = {'editais_verificados': 0, 'fases_alteradas': 0, 'ultimo_check': None}

    async def start(self) -> None:
        self.running = True
        while self.running:
            await self._monitorar_editais()
            self.stats['ultimo_check'] = datetime.utcnow().isoformat()
            await asyncio.sleep(self.check_interval)

    async def stop(self) -> None:
        self.running = False

    async def _monitorar_editais(self) -> None:
        editais = await self.edital_repo.find_ativos()
        agora = datetime.utcnow()
        for edital in editais:
            self.stats['editais_verificados'] += 1
            if edital.fase == FaseEditalCultural.PUBLICADO and agora >= edital.data_inicio_inscricoes:
                edital.abrir_inscricoes()
                await self.edital_repo.save(edital)
                self.stats['fases_alteradas'] += 1
            if edital.fase == FaseEditalCultural.INSCRICOES_ABERTAS and agora > edital.data_fim_inscricoes:
                edital.encerrar_inscricoes()
                await self.edital_repo.save(edital)
                self.stats['fases_alteradas'] += 1