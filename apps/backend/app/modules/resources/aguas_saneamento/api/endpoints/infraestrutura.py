from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.aguas_saneamento.api.deps import get_infraestrutura_service
from app.modules.resources.aguas_saneamento.api.schemas.infraestrutura_schema import InfraestruturaAtivacaoInput, InfraestruturaCreate, InfraestruturaMotivoInput, InfraestruturaResponse
from app.modules.resources.aguas_saneamento.application.services.infraestrutura_service import InfraestruturaService
from app.modules.resources.aguas_saneamento.domain.enums import StatusInfraestrutura, TipoInfraestrutura
from app.modules.resources.aguas_saneamento.exceptions import InfraestruturaAlreadyExistsError, InfraestruturaNotFoundError
router = APIRouter(prefix='/infraestrutura', tags=['Aguas Saneamento - Infraestrutura'])

@router.post('/', response_model=InfraestruturaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_infraestrutura(data: InfraestruturaCreate, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        return await service.registrar(tipo=data.tipo, nome=data.nome, provincia=data.provincia, municipio=data.municipio, capacidade=data.capacidade, unidade_capacidade=data.unidade_capacidade, outorga_id=data.outorga_id, latitude=data.latitude, longitude=data.longitude)
    except InfraestruturaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_infraestrutura:path}/ativar', response_model=InfraestruturaResponse)
async def ativar_infraestrutura(codigo_infraestrutura: str, data: InfraestruturaAtivacaoInput, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        return await service.ativar(codigo_infraestrutura, data_operacao=data.data_operacao)
    except InfraestruturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_infraestrutura:path}/manutencao', response_model=InfraestruturaResponse)
async def manutencao_infraestrutura(codigo_infraestrutura: str, data: InfraestruturaMotivoInput, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        return await service.manutencao(codigo_infraestrutura, motivo=data.motivo)
    except InfraestruturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_infraestrutura:path}/interditar', response_model=InfraestruturaResponse)
async def interditar_infraestrutura(codigo_infraestrutura: str, data: InfraestruturaMotivoInput, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        return await service.interditar(codigo_infraestrutura, motivo=data.motivo)
    except InfraestruturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_infraestrutura:path}/reativar', response_model=InfraestruturaResponse)
async def reativar_infraestrutura(codigo_infraestrutura: str, data: InfraestruturaMotivoInput | None=None, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        motivo = data.motivo if data else None
        return await service.reativar(codigo_infraestrutura, motivo=motivo)
    except InfraestruturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_infraestrutura:path}/desativar', response_model=InfraestruturaResponse)
async def desativar_infraestrutura(codigo_infraestrutura: str, data: InfraestruturaMotivoInput, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        return await service.desativar(codigo_infraestrutura, motivo=data.motivo)
    except InfraestruturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_infraestrutura:path}', response_model=InfraestruturaResponse)
async def obter_infraestrutura(codigo_infraestrutura: str, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    try:
        return await service.obter_por_codigo(codigo_infraestrutura)
    except InfraestruturaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InfraestruturaResponse])
async def listar_infraestruturas(tipo: TipoInfraestrutura | None=None, status_infraestrutura: StatusInfraestrutura | None=None, provincia: str | None=None, municipio: str | None=None, service: InfraestruturaService=Depends(get_infraestrutura_service)):
    return await service.listar(tipo=tipo, status=status_infraestrutura, provincia=provincia, municipio=municipio)