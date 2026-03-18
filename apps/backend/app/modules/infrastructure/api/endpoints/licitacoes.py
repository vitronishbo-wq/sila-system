from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure.api.deps import get_licitacao_service
from apps.backend.app.modules.infrastructure.api.schemas.licitacao_schema import LicitacaoAberturaInput, LicitacaoAdjudicacaoInput, LicitacaoCreate, LicitacaoHomologacaoInput, LicitacaoMotivoInput, LicitacaoResponse
from apps.backend.app.modules.infrastructure.application.services.licitacao_service import LicitacaoService
from apps.backend.app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao
from apps.backend.app.modules.infrastructure.domain.exceptions import LicitacaoAlreadyExistsError, LicitacaoNotFoundError
router = APIRouter(prefix='/licitacoes', tags=['Obras Publicas - Licitacoes'])

@router.post('/', response_model=LicitacaoResponse, status_code=status.HTTP_201_CREATED)
async def abrir_licitacao(data: LicitacaoCreate, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.abrir(objeto=data.objeto, tipo=data.tipo, obra_id=data.obra_id, orgao_responsavel_id=data.orgao_responsavel_id, valor_estimado=data.valor_estimado, data_publicacao_edital=data.data_publicacao_edital, data_entrega_propostas=data.data_entrega_propostas, numero_licitacao=data.numero_licitacao)
    except LicitacaoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/recebimento', response_model=LicitacaoResponse)
async def iniciar_recebimento_licitacao(numero_licitacao: str, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.iniciar_recebimento(numero_licitacao)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/encerrar-recebimento', response_model=LicitacaoResponse)
async def encerrar_recebimento_licitacao(numero_licitacao: str, data: LicitacaoAberturaInput, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.encerrar_recebimento(numero_licitacao, data_abertura=data.data_abertura)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/analise', response_model=LicitacaoResponse)
async def iniciar_analise_licitacao(numero_licitacao: str, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.iniciar_analise(numero_licitacao)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/habilitacao', response_model=LicitacaoResponse)
async def abrir_habilitacao_licitacao(numero_licitacao: str, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.abrir_habilitacao(numero_licitacao)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/recursos', response_model=LicitacaoResponse)
async def iniciar_recursos_licitacao(numero_licitacao: str, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.iniciar_recursos(numero_licitacao)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/adjudicar', response_model=LicitacaoResponse)
async def adjudicar_licitacao(numero_licitacao: str, data: LicitacaoAdjudicacaoInput, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.adjudicar(numero_licitacao, vencedor_id=data.vencedor_id, valor_adjudicado=data.valor_adjudicado)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/homologar', response_model=LicitacaoResponse)
async def homologar_licitacao(numero_licitacao: str, data: LicitacaoHomologacaoInput, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.homologar(numero_licitacao, data_homologacao=data.data_homologacao)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/deserta', response_model=LicitacaoResponse)
async def declarar_deserta_licitacao(numero_licitacao: str, data: LicitacaoMotivoInput, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.declarar_deserta(numero_licitacao, motivo=data.motivo)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/revogar', response_model=LicitacaoResponse)
async def revogar_licitacao(numero_licitacao: str, data: LicitacaoMotivoInput, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.revogar(numero_licitacao, motivo=data.motivo)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{numero_licitacao:path}/anular', response_model=LicitacaoResponse)
async def anular_licitacao(numero_licitacao: str, data: LicitacaoMotivoInput, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.anular(numero_licitacao, motivo=data.motivo)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{numero_licitacao:path}', response_model=LicitacaoResponse)
async def obter_licitacao(numero_licitacao: str, service: LicitacaoService=Depends(get_licitacao_service)):
    try:
        return await service.obter_por_numero(numero_licitacao)
    except LicitacaoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[LicitacaoResponse])
async def listar_licitacoes(status_licitacao: StatusLicitacao | None=None, tipo: TipoLicitacao | None=None, obra_id: UUID | None=None, orgao_responsavel_id: UUID | None=None, service: LicitacaoService=Depends(get_licitacao_service)):
    return await service.listar(status=status_licitacao, tipo=tipo, obra_id=obra_id, orgao_responsavel_id=orgao_responsavel_id)