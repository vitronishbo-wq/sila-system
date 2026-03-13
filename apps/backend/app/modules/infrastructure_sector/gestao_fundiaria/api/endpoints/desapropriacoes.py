from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_desapropriacao_service
from app.modules.infrastructure_sector.gestao_fundiaria.api.schemas.desapropriacao_schema import DesapropriacaoCreate, DesapropriacaoDecretoInput, DesapropriacaoMotivoInput, DesapropriacaoPagamentoInput, DesapropriacaoResponse
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.desapropriacao_service import DesapropriacaoService
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusDesapropriacao, TipoDesapropriacao
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import DesapropriacaoAlreadyExistsError, DesapropriacaoNotFoundError, ImovelNotFoundError
router = APIRouter(prefix='/desapropriacoes', tags=['Gestao Fundiaria - Desapropriacoes'])

def _ensure_adapter_for_reforma_agraria(service: DesapropriacaoService, tipo: TipoDesapropriacao) -> None:
    if tipo == TipoDesapropriacao.REFORMA_AGRARIA and (not service.has_ambiente_adapter()):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Adapter de Ambiente indisponivel para desapropriacao do tipo 'reforma_agraria'. Verifique a integracao do modulo.")

@router.post('/', response_model=DesapropriacaoResponse, status_code=status.HTTP_201_CREATED)
async def instaurar_desapropriacao(data: DesapropriacaoCreate, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    _ensure_adapter_for_reforma_agraria(service, data.tipo)
    try:
        return await service.instaurar(imovel_inscricao=data.imovel_inscricao, tipo=data.tipo, ente_publico=data.ente_publico, finalidade=data.finalidade, valor_indenizacao=data.valor_indenizacao, numero_processo=data.numero_processo)
    except ImovelNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except DesapropriacaoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_processo:path}/decretar', response_model=DesapropriacaoResponse)
async def decretar_desapropriacao(numero_processo: str, data: DesapropriacaoDecretoInput, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    try:
        return await service.decretar(numero_processo, data_decreto=data.data_decreto)
    except DesapropriacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_processo:path}/pagamento', response_model=DesapropriacaoResponse)
async def registrar_pagamento_desapropriacao(numero_processo: str, data: DesapropriacaoPagamentoInput, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    try:
        return await service.registrar_pagamento(numero_processo, data_pagamento=data.data_pagamento)
    except DesapropriacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_processo:path}/encerrar', response_model=DesapropriacaoResponse)
async def encerrar_desapropriacao(numero_processo: str, data: DesapropriacaoMotivoInput, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    try:
        return await service.encerrar(numero_processo, motivo=data.motivo)
    except DesapropriacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_processo:path}/cancelar', response_model=DesapropriacaoResponse)
async def cancelar_desapropriacao(numero_processo: str, data: DesapropriacaoMotivoInput, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    try:
        return await service.cancelar(numero_processo, motivo=data.motivo)
    except DesapropriacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_processo:path}', response_model=DesapropriacaoResponse)
async def obter_desapropriacao(numero_processo: str, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    try:
        return await service.obter_por_numero_processo(numero_processo)
    except DesapropriacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[DesapropriacaoResponse])
async def listar_desapropriacoes(imovel_inscricao: str | None=None, status: StatusDesapropriacao | None=None, ativo: bool | None=None, service: DesapropriacaoService=Depends(get_desapropriacao_service)):
    return await service.listar(imovel_inscricao=imovel_inscricao, status=status, ativo=ativo)