from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.aguas_saneamento.api.deps import get_abastecimento_service
from app.modules.resources.aguas_saneamento.api.schemas.abastecimento_schema import AbastecimentoCreate, AbastecimentoMotivoInput, AbastecimentoOperacaoInput, AbastecimentoResponse
from app.modules.resources.aguas_saneamento.application.services.abastecimento_service import AbastecimentoService
from app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento
from app.modules.resources.aguas_saneamento.exceptions import AbastecimentoAlreadyExistsError, AbastecimentoNotFoundError
router = APIRouter(prefix='/abastecimento', tags=['Aguas Saneamento - Abastecimento'])

@router.post('/', response_model=AbastecimentoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_abastecimento(data: AbastecimentoCreate, service: AbastecimentoService=Depends(get_abastecimento_service)):
    try:
        return await service.registrar(infraestrutura_id=data.infraestrutura_id, nome_sistema=data.nome_sistema, provincia=data.provincia, municipio=data.municipio)
    except AbastecimentoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_abastecimento:path}/iniciar', response_model=AbastecimentoResponse)
async def iniciar_operacao_abastecimento(codigo_abastecimento: str, data: AbastecimentoOperacaoInput, service: AbastecimentoService=Depends(get_abastecimento_service)):
    try:
        return await service.iniciar_operacao(codigo_abastecimento, data_inicio_operacao=data.data_inicio_operacao)
    except AbastecimentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_abastecimento:path}/interromper', response_model=AbastecimentoResponse)
async def interromper_abastecimento(codigo_abastecimento: str, data: AbastecimentoMotivoInput, service: AbastecimentoService=Depends(get_abastecimento_service)):
    try:
        return await service.interromper(codigo_abastecimento, motivo=data.motivo)
    except AbastecimentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_abastecimento:path}/retomar', response_model=AbastecimentoResponse)
async def retomar_abastecimento(codigo_abastecimento: str, service: AbastecimentoService=Depends(get_abastecimento_service)):
    try:
        return await service.retomar(codigo_abastecimento)
    except AbastecimentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{codigo_abastecimento:path}/encerrar', response_model=AbastecimentoResponse)
async def encerrar_abastecimento(codigo_abastecimento: str, data: AbastecimentoMotivoInput, service: AbastecimentoService=Depends(get_abastecimento_service)):
    try:
        return await service.encerrar(codigo_abastecimento, motivo=data.motivo)
    except AbastecimentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{codigo_abastecimento:path}', response_model=AbastecimentoResponse)
async def obter_abastecimento(codigo_abastecimento: str, service: AbastecimentoService=Depends(get_abastecimento_service)):
    try:
        return await service.obter_por_codigo(codigo_abastecimento)
    except AbastecimentoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AbastecimentoResponse])
async def listar_abastecimentos(infraestrutura_id: UUID | None=None, status_abastecimento: StatusAbastecimento | None=None, provincia: str | None=None, municipio: str | None=None, service: AbastecimentoService=Depends(get_abastecimento_service)):
    return await service.listar(infraestrutura_id=infraestrutura_id, status=status_abastecimento, provincia=provincia, municipio=municipio)