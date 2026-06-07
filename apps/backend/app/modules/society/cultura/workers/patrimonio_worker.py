from __future__ import annotations

import asyncio
from datetime import datetime

from apps.backend.app.modules.society.cultura.domain.enums import StatusTombamento


class PatrimonioWorker:
    def __init__(self, *, bem_repo, iphan_adapter=None, check_interval: int = 21600) -> None:
        self.bem_repo = bem_repo
        self.iphan_adapter = iphan_adapter
        self.check_interval = check_interval
        self.running = False
        self.stats = {"bens_verificados": 0, "sincronizados_iphan": 0, "ultimo_check": None}

    async def start(self) -> None:
        self.running = True
        while self.running:
            await self._sincronizar_bens_tombados()
            self.stats["ultimo_check"] = datetime.utcnow().isoformat()
            await asyncio.sleep(self.check_interval)

    async def stop(self) -> None:
        self.running = False

    async def _sincronizar_bens_tombados(self) -> None:
        tombados = await self.bem_repo.list_by_status_tombamento(StatusTombamento.TOMBADO)
        for bem in tombados:
            self.stats["bens_verificados"] += 1
            if self.iphan_adapter is not None:
                await self.iphan_adapter.registrar_bem_tombado(
                    {
                        "bem_id": str(bem.id),
                        "nome": bem.nome,
                        "registro_ipat": bem.registro_ipat,
                        "tipo": bem.tipo.value,
                    }
                )
                self.stats["sincronizados_iphan"] += 1
