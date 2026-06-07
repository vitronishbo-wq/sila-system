from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.infrastructure.api.deps import get_projeto_service
from apps.backend.app.modules.infrastructure.api.schemas.projeto_schema import (
    ProjetoConclusaoInput,
    ProjetoCreate,
    ProjetoInicioInput,
    ProjetoMotivoInput,
    ProjetoResponse,
)
from apps.backend.app.modules.infrastructure.application.services.projeto_service import (
    ProjetoService,
)
from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto
from apps.backend.app.modules.infrastructure.domain.exceptions import (
    ProjetoAlreadyExistsError,
    ProjetoNotFoundError,
)

router = APIRouter(prefix="/projetos", tags=["Obras Publicas - Projetos"])
projeto_service_dep = Depends(get_projeto_service)


@router.post("/", response_model=ProjetoResponse, status_code=status.HTTP_201_CREATED)
async def criar_projeto(
    data: ProjetoCreate, service: ProjetoService = projeto_service_dep
):
    try:
        return await service.criar(
            nome=data.nome,
            tipo=data.tipo,
            orgao_responsavel_id=data.orgao_responsavel_id,
            responsavel_tecnico_id=data.responsavel_tecnico_id,
            valor_estimado=data.valor_estimado,
            data_inicio_prevista=data.data_inicio_prevista,
            data_fim_prevista=data.data_fim_prevista,
            codigo_projeto=data.codigo_projeto,
            obra_id=data.obra_id,
            descricao=data.descricao,
        )
    except ProjetoAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_projeto:path}/aprovar", response_model=ProjetoResponse)
async def aprovar_projeto(
    codigo_projeto: str, service: ProjetoService = projeto_service_dep
):
    try:
        return await service.aprovar(codigo_projeto)
    except ProjetoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_projeto:path}/iniciar", response_model=ProjetoResponse)
async def iniciar_projeto(
    codigo_projeto: str,
    data: ProjetoInicioInput,
    service: ProjetoService = projeto_service_dep,
):
    try:
        return await service.iniciar_execucao(codigo_projeto, data_inicio=data.data_inicio)
    except ProjetoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_projeto:path}/concluir", response_model=ProjetoResponse)
async def concluir_projeto(
    codigo_projeto: str,
    data: ProjetoConclusaoInput,
    service: ProjetoService = projeto_service_dep,
):
    try:
        return await service.concluir(codigo_projeto, data_fim=data.data_fim)
    except ProjetoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_projeto:path}/revisar", response_model=ProjetoResponse)
async def revisar_projeto(
    codigo_projeto: str,
    data: ProjetoMotivoInput,
    service: ProjetoService = projeto_service_dep,
):
    try:
        return await service.revisar(codigo_projeto, motivo=data.motivo)
    except ProjetoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{codigo_projeto:path}/arquivar", response_model=ProjetoResponse)
async def arquivar_projeto(
    codigo_projeto: str,
    data: ProjetoMotivoInput,
    service: ProjetoService = projeto_service_dep,
):
    try:
        return await service.arquivar(codigo_projeto, motivo=data.motivo)
    except ProjetoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{codigo_projeto:path}", response_model=ProjetoResponse)
async def obter_projeto(
    codigo_projeto: str, service: ProjetoService = projeto_service_dep
):
    try:
        return await service.obter_por_codigo(codigo_projeto)
    except ProjetoNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/", response_model=list[ProjetoResponse])
async def listar_projetos(
    status_projeto: StatusProjeto | None = None,
    tipo: TipoProjeto | None = None,
    orgao_responsavel_id: UUID | None = None,
    obra_id: UUID | None = None,
    service: ProjetoService = projeto_service_dep,
):
    return await service.listar(
        status=status_projeto, tipo=tipo, orgao_responsavel_id=orgao_responsavel_id, obra_id=obra_id
    )
