from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from apps.backend.app.modules.governance.cooperacao_internacional.api.deps import (
    get_projeto_service,
)
from apps.backend.app.modules.governance.cooperacao_internacional.api.schemas.projeto_cooperacao_schema import (
    ProjetoCooperacaoCreate,
    ProjetoCooperacaoResponse,
)
from apps.backend.app.modules.governance.cooperacao_internacional.application.services.projeto_cooperacao_service import (
    ProjetoCooperacaoService,
)

router = APIRouter(prefix="/projetos", tags=["Cooperacao Internacional - Projetos"])

projeto_service_dep = Depends(get_projeto_service)


@router.post("/", response_model=ProjetoCooperacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_projeto(
    payload: ProjetoCooperacaoCreate,
    service: ProjetoCooperacaoService = projeto_service_dep,
) -> ProjetoCooperacaoResponse:
    try:
        projeto = await service.criar_projeto(**payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return ProjetoCooperacaoResponse.model_validate(projeto)


@router.post("/{projeto_id}/aprovar", response_model=ProjetoCooperacaoResponse)
async def aprovar_projeto(
    projeto_id: UUID, service: ProjetoCooperacaoService = projeto_service_dep
) -> ProjetoCooperacaoResponse:
    try:
        projeto = await service.aprovar_projeto(projeto_id=projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return ProjetoCooperacaoResponse.model_validate(projeto)


@router.post("/{projeto_id}/iniciar-execucao", response_model=ProjetoCooperacaoResponse)
async def iniciar_execucao(
    projeto_id: UUID, service: ProjetoCooperacaoService = projeto_service_dep
) -> ProjetoCooperacaoResponse:
    try:
        projeto = await service.iniciar_execucao(projeto_id=projeto_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return ProjetoCooperacaoResponse.model_validate(projeto)


@router.get("/", response_model=list[ProjetoCooperacaoResponse])
async def listar_projetos(
    service: ProjetoCooperacaoService = projeto_service_dep,
) -> list[ProjetoCooperacaoResponse]:
    projetos = await service.listar_projetos()
    return [ProjetoCooperacaoResponse.model_validate(item) for item in projetos]