from __future__ import annotations
import inspect
from app.modules.tourism.application.ports.transportes_logistica_service_port import TransportesLogisticaServicePort

class TransportesLogisticaServiceAdapter(TransportesLogisticaServicePort):

    def __init__(self, service):
        self.service = service

    async def list_opcoes_transporte(self, *, origem: str, destino: str) -> list[str]:
        method = getattr(self.service, 'list_opcoes_transporte', None)
        if callable(method):
            result = method(origem=origem, destino=destino)
            if inspect.isawaitable(result):
                result = await result
            return list(result or [])
        return []

    async def estimate_tempo_viagem_horas(self, *, origem: str, destino: str, modal: str | None=None) -> float | None:
        method = getattr(self.service, 'estimate_tempo_viagem_horas', None)
        if callable(method):
            result = method(origem=origem, destino=destino, modal=modal)
            if inspect.isawaitable(result):
                result = await result
            if result is None:
                return None
            return float(result)
        return None
