
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from uuid import UUID
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_notification_service
from app.core.notifications.services.notification_service import NotificationService

# Importações de domínio e integrações conforme a arquitetura SILA
from ..domain.models.bi_event import BIEvent, BIEventType
from ..domain.models.identity_request import RequestStatus
from ..integrations.citizen_fuc_client import CitizenFUCClient
from ..application.services.identity_request_service import IdentityRequestService

# Logger estruturado
logger = logging.getLogger("identidade_civil.api.atestados")

router = APIRouter(prefix="/identidade/atestados", tags=["Identidade Civil - Atestados"])

# Dependências
def get_fuc_client():
    return CitizenFUCClient()

async def get_identity_service(
    db: AsyncSession = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
):
    return IdentityRequestService(db, notification_service=notification_service)

@router.post("/residencia", status_code=status.HTTP_201_CREATED)
async def request_residence_certificate(
    payload: Dict[str, Any], 
    fuc_client: CitizenFUCClient = Depends(get_fuc_client),
    service: IdentityRequestService = Depends(get_identity_service)
):
    """
    Solicita um Atestado de Residência.
    Valida os dados de morada diretamente na projeção soberana do FUC.
    """
    citizen_id = payload.get("citizen_fuc_id")
    operator_id = payload.get("operator_id", "SYSTEM")

    # 1. Consulta Soberania (FUC)
    projection = await fuc_client.get_citizen_by_id(citizen_id)
    if not projection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cidadão não localizado no FUC. Impossível emitir atestado."
        )

    # 2. Criar Processo Administrativo (Service Code 004 - Atestado Residência)
    request = await service.create_request(
        citizen_id=UUID(citizen_id) if isinstance(citizen_id, str) else citizen_id,
        created_by=UUID(operator_id) if operator_id != "SYSTEM" else UUID("00000000-0000-0000-0000-000000000000"),
        request_data={"service_code": "004"}
    )
    
    actor = UUID(operator_id) if operator_id != "SYSTEM" else UUID("00000000-0000-0000-0000-000000000000")
    await service.transition(request.id, RequestStatus.FUC_VALIDATION, f"Dados FUC validados para {projection.fullName}", updated_by=actor)

    # 3. Registro de Evento de Auditoria (O Service já faz auditoria Base, mas aqui é evento de BI específico)
    event = BIEvent.record(
        aggregate_id=str(request.id),
        event_type=BIEventType.DATA_VERIFIED_FUC,
        operator_id=operator_id,
        data={
            "type": "ATESTADO_RESIDENCIA",
            "fuc_sync_id": projection.fucId,
            "verification_timestamp": datetime.utcnow().isoformat()
        }
    )

    await service.transition(request.id, RequestStatus.COMPLETED, updated_by=actor)
    
    # Recarregar para garantir dados atualizados
    request = await service.get_request(request.id, UUID("00000000-0000-0000-0000-000000000000"))

    return {
        "success": True,
        "request_id": str(request.id),
        "service_code": "004",
        "message": "Atestado de Residência gerado com base nos dados soberanos do FUC.",
        "issued_to": projection.fullName,
        "event_id": str(event.id)
    }

@router.post("/vida-e-identidade", status_code=status.HTTP_201_CREATED)
async def request_life_identity_certificate(
    payload: Dict[str, Any], 
    fuc_client: CitizenFUCClient = Depends(get_fuc_client),
    service: IdentityRequestService = Depends(get_identity_service)
):
    """
    Solicita um Atestado de Vida e Identidade.
    Confirma o estado 'Ativo' do cidadão no FUC antes da emissão.
    """
    citizen_id = payload.get("citizen_fuc_id")
    operator_id = payload.get("operator_id", "SYSTEM")

    # 1. Consulta Soberania
    projection = await fuc_client.get_citizen_by_id(citizen_id)
    if not projection:
        raise HTTPException(status_code=404, detail="Soberania FUC não encontrada.")

    # 2. Validar Elegibilidade (Verificar se não consta óbito no FUC)
    is_eligible = await fuc_client.validate_eligibility(citizen_id, "005")
    if not is_eligible:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Cidadão com restrições de soberania no FUC. Emissão negada."
        )

    # 3. Processamento via Service
    request = await service.create_request(
        citizen_id=UUID(citizen_id) if isinstance(citizen_id, str) else citizen_id,
        created_by=UUID(operator_id) if operator_id != "SYSTEM" else UUID("00000000-0000-0000-0000-000000000000"),
        request_data={"service_code": "005"}
    )
    actor = UUID(operator_id) if operator_id != "SYSTEM" else UUID("00000000-0000-0000-0000-000000000000")
    await service.transition(request.id, RequestStatus.COMPLETED, updated_by=actor)
    
    # Evento de Identidade
    BIEvent.record(
        aggregate_id=str(request.id),
        event_type=BIEventType.BI_PROJECTION_SYNCED, # Reuso de tipo de evento para sincronismo
        operator_id=operator_id,
        data={"action": "CERTIFICATE_LIFE_IDENTITY_ISSUED"}
    )

    return {
        "success": True,
        "request_id": str(request.id),
        "service_code": "005",
        "citizen_name": projection.fullName,
        "valid_until": (datetime.utcnow().date()).isoformat() # Validade administrativa curta
    }

@router.get("/{request_id}/status")
async def get_request_status(
    request_id: UUID,
    service: IdentityRequestService = Depends(get_identity_service)
):
    """
    Consulta o estado de um processo de atestado específico.
    """
    request = await service.get_request(request_id, UUID("00000000-0000-0000-0000-000000000000"))
    if not request:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
    return {
        "request_id": str(request.id),
        "current_status": request.status.value if hasattr(request.status, 'value') else request.status,
        "notes": getattr(request, "notes", [])
    }
