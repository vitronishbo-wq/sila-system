from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_citizen
from app.api.dependencies import extract_citizen_id_from_current
from app.citizen.core.services.request_service import RequestService
from app.citizen.core.schemas import RequestCreate, RequestResponse

router = APIRouter(prefix="/requests", tags=["citizen-requests"])

@router.post("/", response_model=RequestResponse)
async def create_request(
    request_data: RequestCreate,
    db: AsyncSession = Depends(get_db),
    citizen_id: UUID = Depends(extract_citizen_id_from_current),
    current_citizen: dict = Depends(get_current_citizen)
) -> RequestResponse:
    """Cria pedido REAL"""
    
    service = RequestService(db)
    
    # Obter territórios do cidadão
    territory_ids = {
        "province_id": current_citizen.get("province_id"),
        "municipality_id": current_citizen.get("municipality_id"),
        "commune_id": current_citizen.get("commune_id")
    }
    
    request = await service.create_request(
        citizen_id=citizen_id,
        service_id=request_data.service_id,
        data=request_data.data,
        territory_ids=territory_ids
    )
    
    return request

@router.get("/", response_model=List[RequestResponse])
async def list_my_requests(
    db: AsyncSession = Depends(get_db),
    citizen_id: UUID = Depends(extract_citizen_id_from_current),
):
    """Lista pedidos REAIS do cidadão"""
    
    service = RequestService(db)
    return await service.get_citizen_requests(citizen_id)

@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    citizen_id: UUID = Depends(extract_citizen_id_from_current),
):
    """Detalhe REAL do pedido"""
    
    service = RequestService(db)
    request = await service.get_request(request_id, citizen_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    return request
