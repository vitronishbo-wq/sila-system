from __future__ import annotations

import inspect

from apps.backend.app.modules.tourism.application.ports.comercio_servicos_service_port import (
    ComercioServicosServicePort,
)


class ComercioServicosServiceAdapter(ComercioServicosServicePort):
    def __init__(self, service):
        self.service = service

    async def list_parceiros_turisticos(self, *, municipio: str) -> list[str]:
        method = getattr(self.service, "list_parceiros_turisticos", None)
        if callable(method):
            result = method(municipio=municipio)
            if inspect.isawaitable(result):
                result = await result
            return list(result or [])
        return []

    async def agencia_cnpj_ativo(self, *, cnpj: str) -> bool:
        method = getattr(self.service, "agencia_cnpj_ativo", None)
        if callable(method):
            result = method(cnpj=cnpj)
            if inspect.isawaitable(result):
                result = await result
            return bool(result)
        return True
