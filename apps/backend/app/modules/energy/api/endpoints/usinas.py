from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.energy.api.deps import get_usina_service
from apps.backend.app.modules.energy.api.schemas.usina_schema import UsinaCreate, UsinaDataInput, UsinaMotivoInput, UsinaPotenciaInput, UsinaResponse
from apps.backend.app.modules.energy.application.services import UsinaService
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusUsina
from apps.backend.app.modules.energy.core.exceptions import InvalidUsinaStateError, UsinaAlreadyExistsError, UsinaNotFoundError
router = APIRouter(prefix='/usinas', tags=['Energia - Usinas'])

@router.post('/', response_model=UsinaResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_usina(data: UsinaCreate, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.cadastrar_usina(codigo_aneel=data.codigo_aneel, nome=data.nome, fonte=data.fonte, tipo=data.tipo, potencia_instalada_mw=data.potencia_instalada_mw, proprietario_id=data.proprietario_id, proprietario_tipo=data.proprietario_tipo, municipio=data.municipio, provincia=data.provincia)
    except UsinaAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{usina_id}/iniciar-construcao', response_model=UsinaResponse)
async def iniciar_construcao(usina_id: UUID, data: UsinaDataInput, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.iniciar_construcao(usina_id, data_inicio=data.data)
    except UsinaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidUsinaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{usina_id}/iniciar-operacao', response_model=UsinaResponse)
async def iniciar_operacao(usina_id: UUID, data: UsinaDataInput, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.iniciar_operacao(usina_id, data_operacao=data.data)
    except UsinaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidUsinaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{usina_id}/paralisar', response_model=UsinaResponse)
async def paralisar_usina(usina_id: UUID, data: UsinaMotivoInput, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.paralisar_usina(usina_id, motivo=data.motivo)
    except UsinaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidUsinaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{usina_id}/desativar', response_model=UsinaResponse)
async def desativar_usina(usina_id: UUID, data: UsinaMotivoInput, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.desativar_usina(usina_id, motivo=data.motivo)
    except UsinaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidUsinaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{usina_id}/potencia-fiscalizada', response_model=UsinaResponse)
async def atualizar_potencia_fiscalizada(usina_id: UUID, data: UsinaPotenciaInput, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.atualizar_potencia_fiscalizada(usina_id, potencia=data.potencia)
    except UsinaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidUsinaStateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{usina_id}', response_model=UsinaResponse)
async def obter_usina(usina_id: UUID, service: UsinaService=Depends(get_usina_service)):
    try:
        return await service.obter_por_id(usina_id)
    except UsinaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[UsinaResponse])
async def listar_usinas(status_usina: StatusUsina | None=None, fonte: FonteEnergia | None=None, provincia: str | None=None, service: UsinaService=Depends(get_usina_service)):
    return await service.listar(status=status_usina, fonte=fonte, provincia=provincia)
