from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.aguas_saneamento.api.deps import get_outorga_service
from app.modules.resources.aguas_saneamento.api.schemas.outorga_schema import OutorgaCreate, OutorgaDeferimentoInput, OutorgaMotivoInput, OutorgaRenovacaoInput, OutorgaResponse
from app.modules.resources.aguas_saneamento.application.services.outorga_service import OutorgaService
from app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoOutorga
from app.modules.resources.aguas_saneamento.exceptions import OutorgaAlreadyExistsError, OutorgaNotFoundError
router = APIRouter(prefix='/outorgas', tags=['Aguas Saneamento - Outorgas'])

@router.post('/', response_model=OutorgaResponse, status_code=status.HTTP_201_CREATED)
async def requerer_outorga(data: OutorgaCreate, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.requerer(tipo=data.tipo, requerente_id=data.requerente_id, requerente_tipo=data.requerente_tipo, corpo_hidrico_id=data.corpo_hidrico_id, tipo_captacao=data.tipo_captacao, vazao=data.vazao, unidade_vazao=data.unidade_vazao, tempo_captacao=data.tempo_captacao, periodo_captacao=data.periodo_captacao, finalidade_uso=data.finalidade_uso, coordenadas_lat=data.coordenadas_lat, coordenadas_long=data.coordenadas_long)
    except OutorgaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_outorga:path}/analise', response_model=OutorgaResponse)
async def iniciar_analise_outorga(numero_outorga: str, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.iniciar_analise(numero_outorga)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_outorga:path}/deferir', response_model=OutorgaResponse)
async def deferir_outorga(numero_outorga: str, data: OutorgaDeferimentoInput, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.deferir(numero_outorga, data_validade_inicio=data.data_validade_inicio, data_validade_fim=data.data_validade_fim, data_publicacao=data.data_publicacao, processo=data.processo)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_outorga:path}/indeferir', response_model=OutorgaResponse)
async def indeferir_outorga(numero_outorga: str, data: OutorgaMotivoInput, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.indeferir(numero_outorga, motivo=data.motivo)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_outorga:path}/suspender', response_model=OutorgaResponse)
async def suspender_outorga(numero_outorga: str, data: OutorgaMotivoInput, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.suspender(numero_outorga, motivo=data.motivo)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_outorga:path}/cancelar', response_model=OutorgaResponse)
async def cancelar_outorga(numero_outorga: str, data: OutorgaMotivoInput, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.cancelar(numero_outorga, motivo=data.motivo)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_outorga:path}/renovar', response_model=OutorgaResponse)
async def renovar_outorga(numero_outorga: str, data: OutorgaRenovacaoInput, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.renovar(numero_outorga, nova_data_fim=data.nova_data_fim)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_outorga:path}', response_model=OutorgaResponse)
async def obter_outorga(numero_outorga: str, service: OutorgaService=Depends(get_outorga_service)):
    try:
        return await service.obter_por_numero(numero_outorga)
    except OutorgaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OutorgaResponse])
async def listar_outorgas(requerente_id: UUID | None=None, tipo: TipoOutorga | None=None, status_outorga: StatusOutorga | None=None, service: OutorgaService=Depends(get_outorga_service)):
    return await service.listar(requerente_id=requerente_id, tipo=tipo, status=status_outorga)