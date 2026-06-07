from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import (
    get_plano_diretor_service,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.schemas.plano_diretor_schema import (
    PlanoDiretorAprovacaoCamaraInput,
    PlanoDiretorAudienciaInput,
    PlanoDiretorCreate,
    PlanoDiretorResponse,
    PlanoDiretorSancaoInput,
    PlanoDiretorValidadeInput,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.plano_diretor_service import (
    PlanoDiretorService,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusPlanoDiretor,
    TipoPlanoDiretor,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import (
    PlanoDiretorAlreadyExistsError,
    PlanoDiretorNotFoundError,
)

router = APIRouter(prefix="/planos-diretores", tags=["Urbanismo Habitacao - Planos Diretores"])
plano_diretor_service_dep = Depends(get_plano_diretor_service)


@router.post("/", response_model=PlanoDiretorResponse, status_code=status.HTTP_201_CREATED)
async def criar_plano_diretor(
    data: PlanoDiretorCreate, service: PlanoDiretorService = plano_diretor_service_dep
):
    try:
        return await service.criar(
            nome=data.nome,
            tipo=data.tipo,
            provincia=data.provincia,
            ano_elaboracao=data.ano_elaboracao,
            orgao_responsavel_id=data.orgao_responsavel_id,
            municipio=data.municipio,
            codigo_plano=data.codigo_plano,
        )
    except PlanoDiretorAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/consulta-publica", response_model=PlanoDiretorResponse)
async def iniciar_consulta_publica(
    codigo_plano: str, service: PlanoDiretorService = plano_diretor_service_dep
):
    try:
        return await service.iniciar_consulta_publica(codigo_plano)
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/audiencia-publica", response_model=PlanoDiretorResponse)
async def realizar_audiencia_publica(
    codigo_plano: str,
    data: PlanoDiretorAudienciaInput,
    service: PlanoDiretorService = plano_diretor_service_dep,
):
    try:
        return await service.realizar_audiencia_publica(
            codigo_plano, participantes=data.participantes
        )
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/aprovar-camara", response_model=PlanoDiretorResponse)
async def aprovar_camara(
    codigo_plano: str,
    data: PlanoDiretorAprovacaoCamaraInput,
    service: PlanoDiretorService = plano_diretor_service_dep,
):
    try:
        return await service.aprovar_camara(
            codigo_plano, lei_aprovacao=data.lei_aprovacao, ano_aprovacao=data.ano_aprovacao
        )
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/aprovar-prefeitura", response_model=PlanoDiretorResponse)
async def aprovar_prefeitura(
    codigo_plano: str, service: PlanoDiretorService = plano_diretor_service_dep
):
    try:
        return await service.aprovar_prefeitura(codigo_plano)
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/sancionar", response_model=PlanoDiretorResponse)
async def sancionar(
    codigo_plano: str,
    data: PlanoDiretorSancaoInput,
    service: PlanoDiretorService = plano_diretor_service_dep,
):
    try:
        return await service.sancionar(codigo_plano, data_publicacao=data.data_publicacao)
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/publicar", response_model=PlanoDiretorResponse)
async def publicar(
    codigo_plano: str, service: PlanoDiretorService = plano_diretor_service_dep
):
    try:
        return await service.publicar(codigo_plano)
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_plano:path}/validade", response_model=PlanoDiretorResponse)
async def definir_validade(
    codigo_plano: str,
    data: PlanoDiretorValidadeInput,
    service: PlanoDiretorService = plano_diretor_service_dep,
):
    try:
        return await service.definir_validade(
            codigo_plano, data_inicio=data.data_inicio, data_fim=data.data_fim
        )
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_plano:path}", response_model=PlanoDiretorResponse)
async def obter_plano_diretor(
    codigo_plano: str, service: PlanoDiretorService = plano_diretor_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_plano)
    except PlanoDiretorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[PlanoDiretorResponse])
async def listar_planos_diretores(
    status_plano: StatusPlanoDiretor | None = None,
    tipo_plano: TipoPlanoDiretor | None = None,
    provincia: str | None = None,
    service: PlanoDiretorService = plano_diretor_service_dep,
):
    return await service.listar(status=status_plano, tipo=tipo_plano, provincia=provincia)
