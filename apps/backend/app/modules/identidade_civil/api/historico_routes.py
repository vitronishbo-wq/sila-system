from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from datetime import datetime, timedelta
import uuid

# Importações de domínio para consistência de tipos
from ..domain.models.bi_event import BIEventType

router = APIRouter(prefix="/identidade/historico", tags=["Identidade Civil - Auditoria"])

@router.get("/{aggregate_id}", response_model=List[Dict[str, Any]])
async def get_event_history(aggregate_id: str):
    """
    Recupera o histórico completo de eventos (Audit Trail) associado a um BI ou Processo.
    Garante a transparência e rastreabilidade exigida pela arquitetura SILA.
    """
    # Validação básica de UUID para o aggregate_id (BI ou Request ID)
    try:
        uuid.UUID(aggregate_id)
    except ValueError:
        # Se não for UUID, pode ser um número de BI formatado, permitimos prosseguir para a busca
        pass

    # Simulação de consulta a um repositório de eventos (Event Store)
    # Em produção: return await event_repository.find_by_aggregate(aggregate_id)
    
    now = datetime.utcnow()
    
    mock_history = [
        {
            "id": str(uuid.uuid4()),
            "aggregate_id": aggregate_id,
            "event_type": BIEventType.REQUEST_CREATED.value,
            "timestamp": (now - timedelta(days=5)).isoformat(),
            "operator_id": "SILA-OP-77",
            "payload": {"service_code": "001", "origin": "Balcão Único"},
            "metadata": {"ip": "10.0.5.12"}
        },
        {
            "id": str(uuid.uuid4()),
            "aggregate_id": aggregate_id,
            "event_type": BIEventType.DATA_VERIFIED_FUC.value,
            "timestamp": (now - timedelta(days=5, hours=2)).isoformat(),
            "operator_id": "SYSTEM",
            "payload": {"fuc_status": "VALID", "integrity_check": "MATCH"},
            "metadata": {"source": "FUC_GATEWAY_V2"}
        },
        {
            "id": str(uuid.uuid4()),
            "aggregate_id": aggregate_id,
            "event_type": BIEventType.BI_APPROVED.value,
            "timestamp": (now - timedelta(days=4)).isoformat(),
            "operator_id": "SILA-SUP-01",
            "payload": {"decision": "APPROVED", "notes": "Documentação conforme"},
            "metadata": {}
        },
        {
            "id": str(uuid.uuid4()),
            "aggregate_id": aggregate_id,
            "event_type": BIEventType.BI_ISSUED.value,
            "timestamp": (now - timedelta(days=1)).isoformat(),
            "operator_id": "SILA-OP-88",
            "payload": {"bi_number": "004567890LA045", "delivery_method": "PRESENTIAL"},
            "metadata": {"location": "Posto Central Luanda"}
        }
    ]

    # Ordenação cronológica invertida (mais recentes primeiro)
    return sorted(mock_history, key=lambda x: x["timestamp"], reverse=True)

@router.get("/tipos/catalogo", response_model=Dict[str, str])
async def get_event_types_catalog():
    """
    Retorna o catálogo de tipos de eventos suportados pelo sistema para uso em filtros da UI.
    """
    return {event.name: event.value for event in BIEventType}
