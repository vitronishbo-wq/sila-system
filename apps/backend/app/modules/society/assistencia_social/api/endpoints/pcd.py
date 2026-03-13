from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, status
from apps.backend.app.modules.society.assistencia_social.api.deps import get_pcd_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import raise_http_for_value_error
from apps.backend.app.modules.society.assistencia_social.api.schemas.pcd_schema import PCDCreate, PCDResponse
from apps.backend.app.modules.society.assistencia_social.application.services.pcd_service import PCDService
router = APIRouter(prefix='/pcd', tags=['Assistencia Social - PcD'])

@router.post('/', response_model=PCDResponse, status_code=status.HTTP_201_CREATED)
async def registrar_pcd(data: PCDCreate, service: PCDService=Depends(get_pcd_service)) -> PCDResponse:
    try:
        return await service.registrar_pcd(beneficiario_id=data.beneficiario_id, citizen_id_pcd=data.citizen_id_pcd, tipo_deficiencia=data.tipo_deficiencia, cid=data.cid, grau_deficiencia=data.grau_deficiencia, laudo_id=data.laudo_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/{item_id}', response_model=PCDResponse)
async def obter_pcd(item_id: UUID, service: PCDService=Depends(get_pcd_service)) -> PCDResponse:
    try:
        return await service.buscar_pcd(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/', response_model=list[PCDResponse])
async def listar_pcd(beneficiario_id: UUID | None=None, service: PCDService=Depends(get_pcd_service)) -> list[PCDResponse]:
    return await service.listar_pcd(beneficiario_id=beneficiario_id)

@router.patch('/{item_id}/ativar-bpc', response_model=PCDResponse)
async def ativar_bpc(item_id: UUID, service: PCDService=Depends(get_pcd_service)) -> PCDResponse:
    try:
        return await service.ativar_bpc(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.patch('/{item_id}/encerrar', response_model=PCDResponse)
async def encerrar_pcd(item_id: UUID, service: PCDService=Depends(get_pcd_service)) -> PCDResponse:
    try:
        return await service.encerrar_pcd(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_pcd(item_id: UUID, service: PCDService=Depends(get_pcd_service)) -> None:
    try:
        await service.remover_pcd(item_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)