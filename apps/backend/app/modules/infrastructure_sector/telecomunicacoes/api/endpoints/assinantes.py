from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_assinante_service
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.assinante_schema import AssinanteCreate, AssinanteResponse, AssinanteStatusUpdate
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.assinante_service import AssinanteService
router = APIRouter(prefix='/assinantes', tags=['Telecomunicacoes - Assinantes'])

@router.post('/', response_model=AssinanteResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_assinante(data: AssinanteCreate, service: AssinanteService=Depends(get_assinante_service)) -> AssinanteResponse:
    try:
        return await service.cadastrar_assinante(operadora_id=data.operadora_id, tipo_plano=data.tipo_plano, servico_principal=data.servico_principal, municipio=data.municipio, provincia=data.provincia, nome=data.nome, citizen_id=data.citizen_id, telefone_contato=data.telefone_contato, email_contato=data.email_contato, contrato_numero=data.contrato_numero, valor_mensal=float(data.valor_mensal) if data.valor_mensal is not None else None, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{assinante_id}', response_model=AssinanteResponse)
async def obter_assinante(assinante_id: UUID, service: AssinanteService=Depends(get_assinante_service)) -> AssinanteResponse:
    try:
        return await service.buscar_assinante(assinante_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AssinanteResponse])
async def listar_assinantes(operadora_id: UUID | None=None, municipio: str | None=None, somente_ativos: bool=True, service: AssinanteService=Depends(get_assinante_service)) -> list[AssinanteResponse]:
    return await service.listar_assinantes(operadora_id=operadora_id, municipio=municipio, somente_ativos=somente_ativos)

@router.patch('/{assinante_id}/status', response_model=AssinanteResponse)
async def atualizar_status_assinante(assinante_id: UUID, data: AssinanteStatusUpdate, service: AssinanteService=Depends(get_assinante_service)) -> AssinanteResponse:
    try:
        return await service.atualizar_status(assinante_id=assinante_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{assinante_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_assinante(assinante_id: UUID, service: AssinanteService=Depends(get_assinante_service)) -> None:
    try:
        await service.remover_assinante(assinante_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))