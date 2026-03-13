from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.modules.society.assistencia_social.api.deps import get_beneficio_service
from app.modules.society.assistencia_social.api.endpoints._errors import raise_http_for_value_error
from app.modules.society.assistencia_social.api.schemas.beneficio_schema import BeneficioBpcPcdCreate, BeneficioCreate, BeneficioMotivo, BeneficioResponse
from app.modules.society.assistencia_social.application.services.beneficio_service import BeneficioService
router = APIRouter(prefix='/beneficios', tags=['Assistencia Social - Beneficios'])

@router.post('/', response_model=BeneficioResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_beneficio(data: BeneficioCreate, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.solicitar_beneficio(beneficiario_id=data.beneficiario_id, tipo=data.tipo, valor=data.valor, programa_social_id=data.programa_social_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.post('/bpc-pcd', response_model=BeneficioResponse, status_code=status.HTTP_201_CREATED)
async def conceder_bpc_pcd(data: BeneficioBpcPcdCreate, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.conceder_bpc_pcd(beneficiario_id=data.beneficiario_id, pcd_id=data.pcd_id, valor=data.valor)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/{beneficio_id}', response_model=BeneficioResponse)
async def obter_beneficio(beneficio_id: UUID, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.buscar_beneficio(beneficio_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/', response_model=list[BeneficioResponse])
async def listar_beneficios(beneficiario_id: UUID | None=None, service: BeneficioService=Depends(get_beneficio_service)) -> list[BeneficioResponse]:
    return await service.listar_beneficios(beneficiario_id=beneficiario_id)

@router.patch('/{beneficio_id}/aprovar', response_model=BeneficioResponse)
async def aprovar_beneficio(beneficio_id: UUID, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.aprovar_beneficio(beneficio_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.patch('/{beneficio_id}/negar', response_model=BeneficioResponse)
async def negar_beneficio(beneficio_id: UUID, data: BeneficioMotivo, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.negar_beneficio(beneficio_id, data.motivo)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.patch('/{beneficio_id}/suspender', response_model=BeneficioResponse)
async def suspender_beneficio(beneficio_id: UUID, data: BeneficioMotivo, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.suspender_beneficio(beneficio_id, data.motivo)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.patch('/{beneficio_id}/encerrar', response_model=BeneficioResponse)
async def encerrar_beneficio(beneficio_id: UUID, data: BeneficioMotivo, service: BeneficioService=Depends(get_beneficio_service)) -> BeneficioResponse:
    try:
        return await service.encerrar_beneficio(beneficio_id, data.motivo)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.delete('/{beneficio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_beneficio(beneficio_id: UUID, service: BeneficioService=Depends(get_beneficio_service)) -> None:
    try:
        await service.remover_beneficio(beneficio_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)