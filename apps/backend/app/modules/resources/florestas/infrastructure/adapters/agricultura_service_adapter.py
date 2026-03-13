from __future__ import annotations
from typing import Any
from apps.backend.app.modules.resources.florestas.application.ports.agricultura_service_port import AgriculturaServicePort
from apps.backend.app.modules.resources.florestas.infrastructure.adapters._integration_runtime import invoke_async_method

class AgriculturaServiceAdapter(AgriculturaServicePort):

    def __init__(self, dependency: object | None=None):
        self.dependency = dependency

    async def available(self) -> bool:
        ok, _ = await invoke_async_method(self.dependency, 'listar')
        return ok

    async def integration_payload(self) -> dict[str, Any]:
        ok, propriedades = await invoke_async_method(self.dependency, 'listar')
        return {'provider': type(self.dependency).__name__ if self.dependency is not None else 'none', 'capability': 'correlacao_uso_solo', 'propriedades_rurais': len(propriedades) if ok and isinstance(propriedades, list) else None}