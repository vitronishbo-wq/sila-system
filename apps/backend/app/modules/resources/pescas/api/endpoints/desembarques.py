from __future__ import annotations
from fastapi import APIRouter, Depends, status
from app.modules.resources.pescas.api.deps import get_desembarque_service
from app.modules.resources.pescas.api.schemas.desembarque_schema import DesembarqueCreate, DesembarqueResponse
from app.modules.resources.pescas.application.services.desembarque_service import DesembarqueService
router = APIRouter(prefix='/desembarques', tags=['Pescas - Desembarques'])

@router.post('/', response_model=DesembarqueResponse, status_code=status.HTTP_201_CREATED)
async def registrar_desembarque(data: DesembarqueCreate, service: DesembarqueService=Depends(get_desembarque_service)):
    return await service.registrar_desembarque(captura_id=data.captura_id, porto_desembarque=data.porto_desembarque, quantidade_kg=data.quantidade_kg)

@router.get('/', response_model=list[DesembarqueResponse])
async def listar_desembarques(service: DesembarqueService=Depends(get_desembarque_service)):
    return await service.listar()