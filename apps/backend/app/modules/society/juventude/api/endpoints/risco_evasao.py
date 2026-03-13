from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.juventude.api.deps import get_risco_evasao_service
from app.modules.society.juventude.api.schemas.risco_evasao_schema import RiscoEvasaoAvaliar, RiscoEvasaoResponse
from app.modules.society.juventude.application.services.risco_evasao_service import RiscoEvasaoService
from app.modules.society.juventude.domain.enums import RiscoSocial
router = APIRouter(prefix='/riscos-evasao', tags=['Juventude - Risco Evasao'])

@router.post('/avaliar', response_model=RiscoEvasaoResponse, status_code=status.HTTP_201_CREATED)
async def avaliar_risco(data: RiscoEvasaoAvaliar, service: RiscoEvasaoService=Depends(get_risco_evasao_service)) -> RiscoEvasaoResponse:
    try:
        return await service.avaliar_risco(jovem_id=data.jovem_id, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.get('/jovem/{jovem_id}/ativo', response_model=RiscoEvasaoResponse)
async def obter_risco_ativo_jovem(jovem_id: UUID, service: RiscoEvasaoService=Depends(get_risco_evasao_service)) -> RiscoEvasaoResponse:
    try:
        return await service.buscar_risco_ativo_por_jovem(jovem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/{risco_id}', response_model=RiscoEvasaoResponse)
async def obter_risco(risco_id: UUID, service: RiscoEvasaoService=Depends(get_risco_evasao_service)) -> RiscoEvasaoResponse:
    try:
        return await service.buscar_risco(risco_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[RiscoEvasaoResponse])
async def listar_riscos(nivel: RiscoSocial | None=None, service: RiscoEvasaoService=Depends(get_risco_evasao_service)) -> list[RiscoEvasaoResponse]:
    return await service.listar_riscos(nivel=nivel)