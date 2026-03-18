from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure.domain_publicas.api.deps import get_edital_service
from apps.backend.app.modules.infrastructure.domain_publicas.api.schemas.edital_schema import EditalCreate, EditalEncerramentoInput, EditalMotivoInput, EditalResponse, EditalRetificacaoInput
from apps.backend.app.modules.infrastructure.domain_publicas.application.services.edital_service import EditalService
from apps.backend.app.modules.infrastructure.domain_publicas.domain.enums import StatusEdital
from apps.backend.app.modules.infrastructure.domain_publicas.exceptions import EditalAlreadyExistsError, EditalNotFoundError
router = APIRouter(prefix='/editais', tags=['Obras Publicas - Editais'])

@router.post('/', response_model=EditalResponse, status_code=status.HTTP_201_CREATED)
async def publicar_edital(data: EditalCreate, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.publicar(titulo=data.titulo, objeto=data.objeto, licitacao_id=data.licitacao_id, data_publicacao=data.data_publicacao, data_abertura=data.data_abertura, data_encerramento=data.data_encerramento, numero_edital=data.numero_edital)
    except EditalAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_edital:path}/impugnar', response_model=EditalResponse)
async def impugnar_edital(numero_edital: str, data: EditalMotivoInput, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.impugnar(numero_edital, motivo=data.motivo)
    except EditalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_edital:path}/retificar', response_model=EditalResponse)
async def retificar_edital(numero_edital: str, data: EditalRetificacaoInput, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.retificar(numero_edital, descricao=data.descricao)
    except EditalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_edital:path}/suspender', response_model=EditalResponse)
async def suspender_edital(numero_edital: str, data: EditalMotivoInput, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.suspender(numero_edital, motivo=data.motivo)
    except EditalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_edital:path}/revogar', response_model=EditalResponse)
async def revogar_edital(numero_edital: str, data: EditalMotivoInput, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.revogar(numero_edital, motivo=data.motivo)
    except EditalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_edital:path}/encerrar', response_model=EditalResponse)
async def encerrar_edital(numero_edital: str, data: EditalEncerramentoInput, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.encerrar(numero_edital, data_encerramento=data.data_encerramento)
    except EditalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_edital:path}', response_model=EditalResponse)
async def obter_edital(numero_edital: str, service: EditalService=Depends(get_edital_service)):
    try:
        return await service.obter_por_numero(numero_edital)
    except EditalNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EditalResponse])
async def listar_editais(status_edital: StatusEdital | None=None, licitacao_id: UUID | None=None, service: EditalService=Depends(get_edital_service)):
    return await service.listar(status=status_edital, licitacao_id=licitacao_id)