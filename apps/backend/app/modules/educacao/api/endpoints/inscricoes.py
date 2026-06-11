from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.api.deps import get_inscricao_service
from apps.backend.app.modules.educacao.api.schemas.inscricao_schema import (
    InscricaoCancelar,
    InscricaoConfirmar,
    InscricaoCreate,
    InscricaoResponse,
)
from apps.backend.app.modules.educacao.application.inscricao_service import InscricaoService
from apps.backend.app.modules.educacao.domain.enums import TipoInscricao
from apps.backend.app.modules.educacao.exceptions import CitizenNotFoundError, EscolaNotFoundError
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.modules.educacao.infrastructure.models.inscricao_model import InscricaoModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access

router = APIRouter(prefix="/inscricoes", tags=["Educacao - Inscricoes"])

current_user_dep = Depends(get_current_user)
inscricao_service_dep = Depends(get_inscricao_service)


async def _check_escola_territory(escola_id, user, db):
    escola = await db.get(EscolaModel, escola_id)
    if escola:
        await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=db)


@router.post("/basica", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_basica(
    data: InscricaoCreate,
    service: InscricaoService = inscricao_service_dep,
    user: dict = current_user_dep,
    db: AsyncSession = Depends(get_db),
):
    await _check_escola_territory(data.escola_id, user, db)
    try:
        return await service.criar_inscricao_basica(
            citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes
        )
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/secundaria", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_secundaria(
    data: InscricaoCreate,
    service: InscricaoService = inscricao_service_dep,
    user: dict = current_user_dep,
    db: AsyncSession = Depends(get_db),
):
    await _check_escola_territory(data.escola_id, user, db)
    try:
        return await service.criar_inscricao_secundaria(
            citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes
        )
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/superior", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_superior(
    data: InscricaoCreate,
    service: InscricaoService = inscricao_service_dep,
    user: dict = current_user_dep,
    db: AsyncSession = Depends(get_db),
):
    await _check_escola_territory(data.escola_id, user, db)
    try:
        return await service.criar_inscricao_superior(
            citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes
        )
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/tecnico", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_inscricao_tecnico(
    data: InscricaoCreate,
    service: InscricaoService = inscricao_service_dep,
    user: dict = current_user_dep,
    db: AsyncSession = Depends(get_db),
):
    await _check_escola_territory(data.escola_id, user, db)
    try:
        return await service.criar_inscricao_tecnico(
            citizen_id=data.citizen_id, escola_id=data.escola_id, observacoes=data.observacoes
        )
    except (CitizenNotFoundError, EscolaNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{inscricao_id}/confirmar", response_model=InscricaoResponse)
async def confirmar_inscricao(
    inscricao_id: UUID,
    data: InscricaoConfirmar,
    service: InscricaoService = inscricao_service_dep,
    user: dict = current_user_dep,
    db: AsyncSession = Depends(get_db),
):
    if not data.confirmacao_documental:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmacao documental obrigatoria"
        )
    inscricao = await db.get(InscricaoModel, inscricao_id)
    if inscricao:
        await _check_escola_territory(inscricao.escola_id, user, db)
    actor_id = UUID(user.get("user_id"))
    try:
        return await service.confirmar_inscricao(inscricao_id, actor_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{inscricao_id}/cancelar", response_model=InscricaoResponse)
async def cancelar_inscricao(
    inscricao_id: UUID,
    data: InscricaoCancelar,
    service: InscricaoService = inscricao_service_dep,
    user: dict = current_user_dep,
    db: AsyncSession = Depends(get_db),
):
    inscricao = await db.get(InscricaoModel, inscricao_id)
    if inscricao:
        await _check_escola_territory(inscricao.escola_id, user, db)
    actor_id = UUID(user.get("user_id"))
    try:
        return await service.cancelar_inscricao(inscricao_id, actor_id, data.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/citizen/{citizen_id}", response_model=list[InscricaoResponse])
async def listar_inscricoes_cidadao(
    citizen_id: UUID,
    tipo: TipoInscricao | None = None,
    service: InscricaoService = inscricao_service_dep,
    _: dict = current_user_dep,
):
    return await service.listar_por_cidadao(citizen_id, tipo)