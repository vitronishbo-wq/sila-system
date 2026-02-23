from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from ..application.services.alter_data_service import AlterDataService
from ..integrations.citizen_fuc_client import CitizenFUCClient

# Segurança e DB
from app.api.deps import get_current_user, get_db
from modules.identity.models.user import User

router = APIRouter(prefix="/identidade/validacao", tags=["Identidade Civil - Validação"])

def get_fuc_client():
    return CitizenFUCClient()

def get_alter_data_service(
    db: AsyncSession = Depends(get_db),
    fuc_client: CitizenFUCClient = Depends(get_fuc_client)
):
    return AlterDataService(session=db, fuc_client=fuc_client)

@router.post("/sincronizar-fuc", status_code=status.HTTP_200_OK)
async def sync_bi_with_fuc(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    service: AlterDataService = Depends(get_alter_data_service)
):
    """
    API do Serviço 003: Sincronização de Dados Biográficos.
    Garante que o BI reflita a projeção soberana atual do FUC.
    """
    citizen_id = payload.get("citizen_fuc_id")
    operator_id = payload.get("operator_id", "SYSTEM")
    data_to_sync = payload.get("updated_data", {})

    if not citizen_id:
        raise HTTPException(status_code=400, detail="citizen_fuc_id é obrigatório.")

    result = await service.execute_data_sync(
        citizen_fuc_id=citizen_id,
        operator_id=operator_id,
        updated_fields=data_to_sync
    )

    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)

    return result

@router.get("/status-fuc/{citizen_id}")
async def check_fuc_connection(citizen_id: str):
    """
    Verifica a disponibilidade da projeção do cidadão no FUC.
    """
    client = CitizenFUCClient()
    projection = await client.get_citizen_by_id(citizen_id)
    
    if not projection:
        return {"status": "DISCONNECTED", "citizen_id": citizen_id}
        
    return {
        "status": "SYNCED",
        "last_sync": projection.sync_timestamp.isoformat(),
        "is_alive": projection.is_alive
    }
