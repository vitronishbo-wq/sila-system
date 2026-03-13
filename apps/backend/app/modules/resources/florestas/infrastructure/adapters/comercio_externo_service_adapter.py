from __future__ import annotations
from typing import Any
from apps.backend.app.modules.resources.florestas.application.ports.comercio_externo_service_port import ComercioExternoServicePort
from apps.backend.app.modules.resources.florestas.infrastructure.adapters._integration_runtime import invoke_async_method

class ComercioExternoServiceAdapter(ComercioExternoServicePort):

    def __init__(self, dependency: object | None=None):
        self.dependency = dependency

    async def available(self) -> bool:
        ok, _ = await invoke_async_method(self.dependency, 'listar')
        return ok

    async def integration_payload(self) -> dict[str, Any]:
        ok, exportadores = await invoke_async_method(self.dependency, 'listar')
        return {'provider': type(self.dependency).__name__ if self.dependency is not None else 'none', 'capability': 'controle_exportacao_madeira', 'exportadores_habilitados': len(exportadores) if ok and isinstance(exportadores, list) else None}