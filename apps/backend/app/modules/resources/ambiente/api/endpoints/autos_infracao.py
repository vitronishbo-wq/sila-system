from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.ambiente.api.deps import get_penalidade_service
from app.modules.resources.ambiente.api.schemas.auto_infracao_schema import AutoInfracaoCreate, AutoInfracaoJulgamentoInput, AutoInfracaoResponse
from app.modules.resources.ambiente.application.services.penalidade_service import PenalidadeService
from app.modules.resources.ambiente.domain.enums import StatusAutoInfracao, TipoAutoInfracao
from app.modules.resources.ambiente.exceptions import AutoInfracaoNotFoundError, FiscalizacaoNotFoundError
router = APIRouter(prefix='/autos-infracao', tags=['Ambiente - Autos Infracao'])

@router.post('/', response_model=AutoInfracaoResponse, status_code=status.HTTP_201_CREATED)
async def lavrar_auto_infracao(data: AutoInfracaoCreate, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.lavrar_auto(numero_fiscalizacao=data.numero_fiscalizacao, tipo=data.tipo, descricao=data.descricao, fiscal_id=data.fiscal_id, valor_multa=data.valor_multa)
    except FiscalizacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_auto:path}/notificar', response_model=AutoInfracaoResponse)
async def notificar_auto_infracao(numero_auto: str, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.notificar_auto(numero_auto)
    except AutoInfracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_auto:path}/recurso', response_model=AutoInfracaoResponse)
async def registrar_recurso_auto_infracao(numero_auto: str, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.registrar_recurso_auto(numero_auto)
    except AutoInfracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_auto:path}/julgar', response_model=AutoInfracaoResponse)
async def julgar_auto_infracao(numero_auto: str, data: AutoInfracaoJulgamentoInput, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.julgar_auto(numero_auto, mantido=data.mantido, observacoes=data.observacoes)
    except AutoInfracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_auto:path}', response_model=AutoInfracaoResponse)
async def obter_auto_infracao(numero_auto: str, service: PenalidadeService=Depends(get_penalidade_service)):
    try:
        return await service.obter_auto_por_numero(numero_auto)
    except AutoInfracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AutoInfracaoResponse])
async def listar_autos_infracao(numero_fiscalizacao: str | None=None, tipo: TipoAutoInfracao | None=None, status_auto: StatusAutoInfracao | None=None, service: PenalidadeService=Depends(get_penalidade_service)):
    return await service.listar_autos(numero_fiscalizacao=numero_fiscalizacao, tipo=tipo, status=status_auto)