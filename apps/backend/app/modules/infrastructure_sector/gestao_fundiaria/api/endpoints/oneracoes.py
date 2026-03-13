from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_oneracao_service
from app.modules.infrastructure_sector.gestao_fundiaria.api.schemas.oneracao_schema import OneracaoCreate, OneracaoMotivoInput, OneracaoResponse
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.oneracao_service import OneracaoService
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusOneracao, TipoOneracao
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ImovelNotFoundError, OneracaoAlreadyExistsError, OneracaoNotFoundError
router = APIRouter(prefix='/oneracoes', tags=['Gestao Fundiaria - Oneracoes'])

def _ensure_adapter_for_penhora(service: OneracaoService, tipo: TipoOneracao) -> None:
    if tipo == TipoOneracao.PENHORA and (not service.has_justica_adapter()):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Adapter de Justica indisponivel para registrar oneracao do tipo 'penhora'. Verifique a integracao do modulo.")

@router.post('/', response_model=OneracaoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_oneracao(data: OneracaoCreate, service: OneracaoService=Depends(get_oneracao_service)):
    _ensure_adapter_for_penhora(service, data.tipo)
    try:
        return await service.registrar(imovel_inscricao=data.imovel_inscricao, tipo=data.tipo, credor_nome=data.credor_nome, valor=data.valor, documento_credor=data.documento_credor, data_vencimento=data.data_vencimento, descricao=data.descricao, numero_oneracao=data.numero_oneracao)
    except (ImovelNotFoundError, OneracaoNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except OneracaoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_oneracao:path}/baixar', response_model=OneracaoResponse)
async def baixar_oneracao(numero_oneracao: str, data: OneracaoMotivoInput, service: OneracaoService=Depends(get_oneracao_service)):
    try:
        return await service.baixar(numero_oneracao, motivo=data.motivo)
    except OneracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_oneracao:path}/cancelar', response_model=OneracaoResponse)
async def cancelar_oneracao(numero_oneracao: str, data: OneracaoMotivoInput, service: OneracaoService=Depends(get_oneracao_service)):
    try:
        return await service.cancelar(numero_oneracao, motivo=data.motivo)
    except OneracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_oneracao:path}', response_model=OneracaoResponse)
async def obter_oneracao(numero_oneracao: str, service: OneracaoService=Depends(get_oneracao_service)):
    try:
        return await service.obter_por_numero(numero_oneracao)
    except OneracaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OneracaoResponse])
async def listar_oneracoes(imovel_inscricao: str | None=None, status: StatusOneracao | None=None, ativo: bool | None=None, service: OneracaoService=Depends(get_oneracao_service)):
    return await service.listar(imovel_inscricao=imovel_inscricao, status=status, ativo=ativo)