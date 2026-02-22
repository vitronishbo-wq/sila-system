"""
Routing Engine - Motor de Roteamiento Automático de Pedidos
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session


class RequestState(str, Enum):
    """Estados posibles de una solicitud"""
    # Estados iniciales
    SUBMETIDO = "SUBMETIDO"
    EM_ANALISE_COMUNAL = "EM_ANALISE_COMUNAL"
    EM_ANALISE_MUNICIPAL = "EM_ANALISE_MUNICIPAL"
    EM_ANALISE_PROVINCIAL = "EM_ANALISE_PROVINCIAL"
    EM_ANALISE_CENTRAL = "EM_ANALISE_CENTRAL"
    
    # Estados de escalación
    ESCALADO_MUNICIPIO = "ESCALADO_MUNICIPIO"
    ESCALADO_PROVINCIA = "ESCALADO_PROVINCIA"
    ESCALADO_CENTRAL = "ESCALADO_CENTRAL"
    
    # Esperando cidadão
    AGUARDANDO_CIDADAO_COMUNAL = "AGUARDANDO_CIDADAO_COMUNAL"
    AGUARDANDO_CIDADAO_MUNICIPAL = "AGUARDANDO_CIDADAO_MUNICIPAL"
    AGUARDANDO_CIDADAO_PROVINCIAL = "AGUARDANDO_CIDADAO_PROVINCIAL"
    
    # Estados terminais
    RESOLVIDO = "RESOLVIDO"
    REJEITADO = "REJEITADO"
    CANCELADO = "CANCELADO"
    
    @classmethod
    def initial_states(cls):
        """Estados iniciales cuando se crea un pedido"""
        return [
            cls.EM_ANALISE_COMUNAL,
            cls.EM_ANALISE_MUNICIPAL,
            cls.EM_ANALISE_PROVINCIAL,
            cls.EM_ANALISE_CENTRAL
        ]
    
    @classmethod
    def terminal_states(cls):
        """Estados finales - no hay más transiciones"""
        return [cls.RESOLVIDO, cls.REJEITADO, cls.CANCELADO]
    
    @classmethod
    def waiting_states(cls):
        """Estados esperando acción do cidadão"""
        return [
            cls.AGUARDANDO_CIDADAO_COMUNAL,
            cls.AGUARDANDO_CIDADAO_MUNICIPAL,
            cls.AGUARDANDO_CIDADAO_PROVINCIAL
        ]
    
    @classmethod
    def analysis_states(cls):
        """Estados em análise"""
        return [
            cls.EM_ANALISE_COMUNAL,
            cls.EM_ANALISE_MUNICIPAL,
            cls.EM_ANALISE_PROVINCIAL,
            cls.EM_ANALISE_CENTRAL
        ]


class RoutingRule(str, Enum):
    """Regras de competencia para serviços"""
    COMUNA_ONLY = "COMUNA_ONLY"
    MUNICIPIO_ONLY = "MUNICIPIO_ONLY"
    PROVINCIA_ONLY = "PROVINCIA_ONLY"
    COMUNA_ESCALABLE = "COMUNA_ESCALABLE"
    MUNICIPIO_ESCALABLE = "MUNICIPIO_ESCALABLE"


@dataclass
class RoutingDecision:
    """Decisión de roteamiento"""
    target_territory_id: UUID
    target_territory_type: str
    target_territory_name: str
    initial_state: RequestState
    justification: str
    routing_path: List[str]
    competence_level: str


class RoutingEngine:
    """Motor de roteamiento automático"""
    
    def __init__(self, db: Session, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
    
    def route(self, citizen_id: UUID, citizen_territory_id: UUID, service_id: UUID, request_data: dict):
        """Determina automáticamente para dónde debe ir el pedido"""
        # Implementación será hecha después
        pass
    
    def _apply_routing_rules(self, territory, service, routing_rule: RoutingRule, request_data: dict) -> RoutingDecision:
        """Aplica reglas de roteamiento específicas"""
        if routing_rule == RoutingRule.COMUNA_ONLY:
            commune = self._get_commune_of_citizen(territory)
            return RoutingDecision(
                target_territory_id=commune.id,
                target_territory_type="COMUNA",
                target_territory_name=commune.name,
                initial_state=RequestState.EM_ANALISE_COMUNAL,
                justification="Serviço com competência exclusiva comunal",
                routing_path=["BAIRRO", "COMUNA"],
                competence_level="COMUNA_ONLY"
            )
        return None
    
    def _get_commune_of_citizen(self, territory):
        """Obtiene la comuna del ciudadano"""
        # Implementación será hecha después
        pass
    
    def _get_municipality_of_citizen(self, territory):
        """Obtiene el municipio del ciudadano"""
        pass
    
    def _get_province_of_citizen(self, territory):
        """Obtiene la provincia del ciudadano"""
        pass


class RequestWorkflow:
    """Gerencia el ciclo de vida de un pedido"""
    
    def __init__(self, db: Session, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db
        self.routing_engine = RoutingEngine(db)
    
    def create_request(self, citizen_id: UUID, citizen_territory_id: UUID, service_id: UUID, request_data: dict):
        """Crea un nuevo pedido"""
        # Implementación será hecha después
        pass
    
    def escalate(self, request_id: UUID, reason: str):
        """Escala un pedido al siguiente nivel"""
        pass
    
    def resolve(self, request_id: UUID, resolution: str):
        """Marca un pedido como resuelto"""
        pass
    
    def _get_parent_territory(self, territory_id: UUID):
        """Obtiene el territorio padre en la jerarquía"""
        pass
    
    def _get_central_territory(self):
        """Obtiene el territorio central (nacional)"""
        pass
