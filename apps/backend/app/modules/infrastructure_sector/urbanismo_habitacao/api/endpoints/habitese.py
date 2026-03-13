from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_habite_se_service
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.habite_se_schema import HabiteSeCreate, HabiteSeEmissaoInput, HabiteSeMotivoInput, HabiteSeResponse, HabiteSeVistoriaInput
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.habite_se_service import HabiteSeService
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusHabiteSe, TipoHabiteSe
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import HabiteSeAlreadyExistsError, HabiteSeNotFoundError
router = APIRouter(prefix='/habitese', tags=['Urbanismo Habitacao - Habite-se'])

@router.post('/', response_model=HabiteSeResponse, status_code=status.HTTP_201_CREATED)
async def criar_habite_se(data: HabiteSeCreate, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.criar(numero_processo=data.numero_processo, tipo=data.tipo, alvara_id=data.alvara_id, requerente_id=data.requerente_id, provincia=data.provincia, municipio=data.municipio, endereco_imovel=data.endereco_imovel, area_vistoriada=data.area_vistoriada, codigo_habite_se=data.codigo_habite_se)
    except HabiteSeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_habite_se:path}/agendar-vistoria', response_model=HabiteSeResponse)
async def agendar_vistoria_habite_se(codigo_habite_se: str, data: HabiteSeVistoriaInput, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.agendar_vistoria(codigo_habite_se, data_vistoria=data.data_vistoria, tecnico_vistoriador_id=data.tecnico_vistoriador_id)
    except HabiteSeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_habite_se:path}/aprovar-vistoria', response_model=HabiteSeResponse)
async def aprovar_vistoria_habite_se(codigo_habite_se: str, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.aprovar_vistoria(codigo_habite_se)
    except HabiteSeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_habite_se:path}/reprovar-vistoria', response_model=HabiteSeResponse)
async def reprovar_vistoria_habite_se(codigo_habite_se: str, data: HabiteSeMotivoInput, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.reprovar_vistoria(codigo_habite_se, motivo=data.motivo)
    except HabiteSeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_habite_se:path}/emitir', response_model=HabiteSeResponse)
async def emitir_habite_se(codigo_habite_se: str, data: HabiteSeEmissaoInput, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.emitir(codigo_habite_se, data_emissao=data.data_emissao, data_validade=data.data_validade)
    except HabiteSeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_habite_se:path}/cancelar', response_model=HabiteSeResponse)
async def cancelar_habite_se(codigo_habite_se: str, data: HabiteSeMotivoInput, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.cancelar(codigo_habite_se, motivo=data.motivo)
    except HabiteSeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_habite_se:path}', response_model=HabiteSeResponse)
async def obter_habite_se(codigo_habite_se: str, service: HabiteSeService=Depends(get_habite_se_service)):
    try:
        return await service.obter_por_codigo(codigo_habite_se)
    except HabiteSeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[HabiteSeResponse])
async def listar_habite_se(status_habite_se: StatusHabiteSe | None=None, tipo_habite_se: TipoHabiteSe | None=None, provincia: str | None=None, service: HabiteSeService=Depends(get_habite_se_service)):
    return await service.listar(status=status_habite_se, tipo=tipo_habite_se, provincia=provincia)