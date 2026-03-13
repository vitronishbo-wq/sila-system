from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.ambiente.api.deps import get_fiscalizacao_service
from app.modules.resources.ambiente.api.schemas.fiscalizacao_schema import FiscalizacaoCancelamentoInput, FiscalizacaoConclusaoInput, FiscalizacaoCreate, FiscalizacaoResponse
from app.modules.resources.ambiente.application.services.fiscalizacao_service import FiscalizacaoService
from app.modules.resources.ambiente.domain.enums import StatusFiscalizacao
from app.modules.resources.ambiente.exceptions import FiscalizacaoNotFoundError, LicencaNotFoundError
router = APIRouter(prefix='/fiscalizacoes', tags=['Ambiente - Fiscalizacoes'])

@router.post('/', response_model=FiscalizacaoResponse, status_code=status.HTTP_201_CREATED)
async def agendar_fiscalizacao(data: FiscalizacaoCreate, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    try:
        return await service.agendar(numero_licenca=data.numero_licenca, localidade=data.localidade, objetivo=data.objetivo, fiscal_responsavel=data.fiscal_responsavel, data_agendada=data.data_agendada)
    except LicencaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_fiscalizacao:path}/iniciar', response_model=FiscalizacaoResponse)
async def iniciar_fiscalizacao(numero_fiscalizacao: str, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    try:
        return await service.iniciar(numero_fiscalizacao)
    except FiscalizacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_fiscalizacao:path}/concluir', response_model=FiscalizacaoResponse)
async def concluir_fiscalizacao(numero_fiscalizacao: str, data: FiscalizacaoConclusaoInput, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    try:
        return await service.concluir(numero_fiscalizacao, data.relatorio)
    except FiscalizacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_fiscalizacao:path}/cancelar', response_model=FiscalizacaoResponse)
async def cancelar_fiscalizacao(numero_fiscalizacao: str, data: FiscalizacaoCancelamentoInput, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    try:
        return await service.cancelar(numero_fiscalizacao, data.motivo)
    except FiscalizacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_fiscalizacao:path}', response_model=FiscalizacaoResponse)
async def obter_fiscalizacao(numero_fiscalizacao: str, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    try:
        return await service.obter_por_numero(numero_fiscalizacao)
    except FiscalizacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[FiscalizacaoResponse])
async def listar_fiscalizacoes(numero_licenca: str | None=None, status_fiscalizacao: StatusFiscalizacao | None=None, service: FiscalizacaoService=Depends(get_fiscalizacao_service)):
    return await service.listar(numero_licenca=numero_licenca, status=status_fiscalizacao)