from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RequestState(str, Enum):
    EM_ANALISE_COMUNAL = "EM_ANALISE_COMUNAL"
    EM_ANALISE_MUNICIPAL = "EM_ANALISE_MUNICIPAL"
    EM_ANALISE_PROVINCIAL = "EM_ANALISE_PROVINCIAL"
    EM_ANALISE_NACIONAL = "EM_ANALISE_NACIONAL"
    ROUTED = "ROUTED"
    RESOLVIDO = "RESOLVIDO"
    REJEITADO = "REJEITADO"
    COMPLETED = "COMPLETED"

    @classmethod
    def initial_states(cls):
        return [
            cls.EM_ANALISE_COMUNAL,
            cls.EM_ANALISE_MUNICIPAL,
            cls.EM_ANALISE_PROVINCIAL,
            cls.EM_ANALISE_NACIONAL,
        ]

    @classmethod
    def terminal_states(cls):
        return [cls.RESOLVIDO, cls.REJEITADO, cls.COMPLETED]

    @classmethod
    def waiting_states(cls):
        return [cls.EM_ANALISE_MUNICIPAL, cls.EM_ANALISE_PROVINCIAL, cls.EM_ANALISE_NACIONAL]


@dataclass
class RoutingRule:
    document_type: str
    target_service: str
    state: Optional[RequestState] = None
    priority: int = 0

    COMUNA_ONLY = "COMUNA_ONLY"
    COMUNA_ESCALABLE = "COMUNA_ESCALABLE"
    MUNICIPIO_ONLY = "MUNICIPIO_ONLY"
    MUNICIPIO_ESCALABLE = "MUNICIPIO_ESCALABLE"
    PROVINCIA_ONLY = "PROVINCIA_ONLY"
    NACIONAL = "NACIONAL"
    INTERNACIONAL = "INTERNACIONAL"


class RoutingEngine:
    """Simple routing engine for civil registry flows."""

    def __init__(self):
        self.routes = {}

    def register(self, document_type, handler):
        self.routes[document_type] = handler

    def resolve(self, document_type):
        return self.routes.get(document_type)

    def route(self, document_type, *args, **kwargs):
        handler = self.resolve(document_type)
        if callable(handler):
            return handler(*args, **kwargs)
        return handler


RoutingEngineService = RoutingEngine

__all__ = ["RequestState", "RoutingRule", "RoutingEngine", "RoutingEngineService"]
