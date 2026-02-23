from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict
import uuid

class BIEventType(Enum):
    """
    Catálogo exaustivo de tipos de eventos de Identidade Civil.
    Estes eventos representam factos imutáveis no ciclo de vida de um documento ou processo.
    """
    # Fluxo de Pedido
    REQUEST_CREATED = "REQUEST_CREATED"           # Pedido inicial de serviço (001, 002, etc.)
    DATA_VERIFIED_FUC = "DATA_VERIFIED_FUC"       # Dados validados contra a soberania do FUC
    BI_PROJECTION_SYNCED = "BI_PROJECTION_SYNCED" # Sincronização de dados biográficos FUC -> Identidade
    
    # Fluxo Administrativo
    BI_APPROVED = "BI_APPROVED"                   # Aprovação após verificação de elegibilidade
    BI_REJECTED = "BI_REJECTED"                   # Rejeição administrativa ou por divergência FUC
    
    # Fluxo de Produção e Entrega
    BI_PRINTED = "BI_PRINTED"                     # Documento físico produzido/personalizado
    BI_ISSUED = "BI_ISSUED"                       # Documento entregue e ativado digitalmente
    
    # Manutenção e Ciclo de Vida
    BI_RENEWED = "BI_RENEWED"                     # Renovação (Gera novo BI_ISSUED para nova versão)
    BI_CANCELLED = "BI_CANCELLED"                 # Cancelamento (Óbito, Fraude, Decisão Judicial)
    LOST_REPORTED = "LOST_REPORTED"               # Participação de extravio ou roubo
    SUSPENDED = "SUSPENDED"                       # Suspensão temporária por investigação

@dataclass(frozen=True)
class BIEvent:
    """
    Representação de um Evento de Domínio Imutável.
    Garante que toda ação sobre a Identidade Civil seja auditável e possa ser reconstruída.
    """
    aggregate_id: str  # ID do BI ou do Processo (IdentityRequest)
    event_type: BIEventType
    operator_id: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def record(cls, aggregate_id: str, event_type: BIEventType, operator_id: str, data: Dict[str, Any]) -> "BIEvent":
        """
        Fábrica para registro formal de eventos.
        Garante a integridade mínima dos dados de auditoria.
        """
        return cls(
            aggregate_id=aggregate_id,
            event_type=event_type,
            operator_id=operator_id,
            payload=data,
            metadata={
                "system_version": "2.1.1",
                "origin_module": "identidade_civil"
            }
        )

    @classmethod
    def create(cls, aggregate_id: str, event_type: BIEventType, operator_id: str, **data) -> "BIEvent":
        """
        Helper para criação rápida de eventos via argumentos nomeados.
        """
        return cls.record(aggregate_id, event_type, operator_id, data)
