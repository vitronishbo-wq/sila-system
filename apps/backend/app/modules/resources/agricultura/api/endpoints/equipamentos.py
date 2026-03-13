from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.agricultura.api.deps import get_equipamento_service
from app.modules.resources.agricultura.api.schemas.equipamento_schema import EquipamentoCreate, EquipamentoResponse, UsoEquipamentoInput
from app.modules.resources.agricultura.application.services.equipamento_service import EquipamentoService
from app.modules.resources.agricultura.domain.enums import StatusEquipamento, TipoEquipamento
from app.modules.resources.agricultura.exceptions import EquipamentoNotFoundError
router = APIRouter(prefix='/equipamentos', tags=['Agricultura - equipamentos'])

@router.post('/', response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_equipamento(data: EquipamentoCreate, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.cadastrar(nome=data.nome, tipo=data.tipo, fabricante=data.fabricante, modelo=data.modelo, ano_fabricacao=data.ano_fabricacao, data_aquisicao=data.data_aquisicao)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_equipamento:path}/iniciar-uso', response_model=EquipamentoResponse)
async def iniciar_uso(codigo_equipamento: str, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.iniciar_uso(codigo_equipamento)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_equipamento:path}/registrar-uso', response_model=EquipamentoResponse)
async def registrar_uso(codigo_equipamento: str, data: UsoEquipamentoInput, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.registrar_uso(codigo_equipamento, horas=data.horas)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_equipamento:path}/finalizar-uso', response_model=EquipamentoResponse)
async def finalizar_uso(codigo_equipamento: str, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.finalizar_uso(codigo_equipamento)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_equipamento:path}/enviar-manutencao', response_model=EquipamentoResponse)
async def enviar_manutencao(codigo_equipamento: str, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.enviar_manutencao(codigo_equipamento)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_equipamento:path}/concluir-manutencao', response_model=EquipamentoResponse)
async def concluir_manutencao(codigo_equipamento: str, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.concluir_manutencao(codigo_equipamento)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_equipamento:path}/inativar', response_model=EquipamentoResponse)
async def inativar_equipamento(codigo_equipamento: str, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.inativar(codigo_equipamento)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_equipamento:path}', response_model=EquipamentoResponse)
async def obter_equipamento(codigo_equipamento: str, service: EquipamentoService=Depends(get_equipamento_service)):
    try:
        return await service.obter(codigo_equipamento)
    except EquipamentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EquipamentoResponse])
async def listar_equipamentos(status_equipamento: StatusEquipamento | None=None, tipo_equipamento: TipoEquipamento | None=None, service: EquipamentoService=Depends(get_equipamento_service)):
    return await service.listar(status=status_equipamento, tipo=tipo_equipamento)