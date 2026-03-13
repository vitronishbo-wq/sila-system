from __future__ import annotations
from typing import Any
from app.modules.resources.florestas.application.ports.energia_service_port import EnergiaServicePort
from app.modules.resources.florestas.infrastructure.adapters._integration_runtime import invoke_async_method

class EnergiaServiceAdapter(EnergiaServicePort):

    def __init__(self, dependency: object | None=None):
        self.dependency = dependency

    async def available(self) -> bool:
        ok, _ = await invoke_async_method(self.dependency, 'get_visao_consolidada')
        return ok

    async def integration_payload(self) -> dict[str, Any]:
        ok, visao = await invoke_async_method(self.dependency, 'get_visao_consolidada')
        centrais = len(visao.get('centrais', [])) if ok and isinstance(visao, dict) else None
        subestacoes = len(visao.get('subestacoes', [])) if ok and isinstance(visao, dict) else None
        linhas = len(visao.get('linhas', [])) if ok and isinstance(visao, dict) else None
        return {'provider': type(self.dependency).__name__ if self.dependency is not None else 'none', 'capability': 'restricoes_infraestrutura_energetica', 'centrais': centrais, 'subestacoes': subestacoes, 'linhas_transmissao': linhas}