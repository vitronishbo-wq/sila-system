from __future__ import annotations
import inspect
from app.modules.resources.pescas.industrial.application.ports.industria_service_port import IndustriaServicePort

class IndustriaServiceAdapter(IndustriaServicePort):

    def __init__(self, service):
        self._service = service

    async def cnpj_ativo(self, cnpj: str) -> bool:
        method = getattr(self._service, 'obter_por_cnpj', None)
        if callable(method):
            result = method(cnpj)
            if inspect.isawaitable(result):
                result = await result
            return result is not None
        repo = getattr(self._service, '_repository', None)
        repo_get = getattr(repo, 'get_by_cnpj', None)
        if callable(repo_get):
            result = repo_get(cnpj)
            if inspect.isawaitable(result):
                result = await result
            return result is not None
        return True