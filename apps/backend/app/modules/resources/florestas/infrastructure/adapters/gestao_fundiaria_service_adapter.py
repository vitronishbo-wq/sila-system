from __future__ import annotations
from typing import Any
from apps.backend.app.modules.resources.florestas.application.ports.gestao_fundiaria_service_port import GestaoFundiariaServicePort
from apps.backend.app.modules.resources.florestas.infrastructure.adapters._integration_runtime import invoke_async_method

class GestaoFundiariaServiceAdapter(GestaoFundiariaServicePort):

    def __init__(self, dependency: object | None=None):
        self.dependency = dependency

    async def available(self) -> bool:
        ok, _ = await invoke_async_method(self.dependency, 'listar')
        return ok

    async def integration_payload(self) -> dict[str, Any]:
        ok, imoveis = await invoke_async_method(self.dependency, 'listar')
        return {'provider': type(self.dependency).__name__ if self.dependency is not None else 'none', 'capability': 'cadastro_imoveis_car', 'imoveis_registrados': len(imoveis) if ok and isinstance(imoveis, list) else None}