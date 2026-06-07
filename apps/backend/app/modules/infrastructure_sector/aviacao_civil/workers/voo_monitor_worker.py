from __future__ import annotations

import asyncio
from datetime import datetime, timedelta

from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import StatusVoo


class VooMonitorWorker:
    def __init__(self, *, voo_repo, decea_adapter=None, check_interval: int = 60) -> None:
        self.voo_repo = voo_repo
        self.decea = decea_adapter
        self.check_interval = check_interval
        self.running = False
        self.stats = {"voos_monitorados": 0, "alertas_emitidos": 0, "ultimo_check": None}

    async def start(self) -> None:
        self.running = True
        while self.running:
            await self._monitorar_voos()
            self.stats["ultimo_check"] = datetime.utcnow().isoformat()
            await asyncio.sleep(self.check_interval)

    async def stop(self) -> None:
        self.running = False

    async def _monitorar_voos(self) -> None:
        ativos = await self.voo_repo.find_by_status(StatusVoo.EM_VOO)
        self.stats["voos_monitorados"] += len(ativos)
        for voo in ativos:
            await self._verificar_voo(voo)
        programados = await self.voo_repo.find_by_status(StatusVoo.PROGRAMADO)
        limite = datetime.utcnow() - timedelta(hours=1)
        for voo in programados:
            if voo.data_hora_partida_programada < limite:
                voo.atualizar_status(StatusVoo.ATRASADO, "Nao decolou no horario")
                await self.voo_repo.save(voo)
                self.stats["alertas_emitidos"] += 1

    async def _verificar_voo(self, voo) -> None:
        if self.decea is None:
            return
        posicao = await self.decea.consultar_posicao(voo.numero_voo)
        if not posicao:
            return
        if posicao.get("desviado"):
            voo.atualizar_status(StatusVoo.DIVERTIDO, "Desvio de rota")
            await self.voo_repo.save(voo)
            self.stats["alertas_emitidos"] += 1
