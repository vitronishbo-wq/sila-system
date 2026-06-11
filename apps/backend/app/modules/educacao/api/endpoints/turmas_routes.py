from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
# Importa o novo schema TurmaUpdate
from apps.backend.app.modules.educacao.api.schemas.turma_schema import (
    TurmaCreate,
    TurmaResponse,
    TurmaUpdate,
)
# Importa o modelo de capacidade para a validação
from apps.backend.app.modules.educacao.infrastructure.models.capacity_model import Capacity
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.modules.educacao.infrastructure.models.turma_model import TurmaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access

router = APIRouter(prefix="/turmas", tags=["Educacao - Turmas"])


@router.post("/", response_model=TurmaResponse, status_code=status.HTTP_201_CREATED)
async def criar_turma(
    data: TurmaCreate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    # ... (implementação existente mantida)
    escola = await session.get(EscolaModel, data.escola_id)
    if not escola:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escola nao encontrada")
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=session)

    turma = TurmaModel(
        escola_id=data.escola_id,
        ano_letivo_id=data.ano_letivo_id,
        codigo=data.codigo,
        classe=data.classe,
        turno=data.turno,
        capacidade=data.capacidade,
        ativa=True,
    )
    session.add(turma)
    await session.flush()
    await session.refresh(turma)
    await session.commit()
    return TurmaResponse.from_orm(turma)


@router.patch("/{turma_id}", response_model=TurmaResponse)
async def atualizar_turma(
    turma_id: UUID,
    data: TurmaUpdate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Atualiza uma turma de forma segura, impedindo a redução da capacidade 
    abaixo do número de alunos já matriculados.
    """
    turma = await session.get(TurmaModel, turma_id)
    if not turma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turma nao encontrada")

    # Validação de acesso territorial
    escola = await session.get(EscolaModel, turma.escola_id)
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola, "territory_id", None), db=session)

    # Guarda de Validação de Capacidade
    if data.capacidade is not None:
        # O ID da capacidade pode ser o mesmo da turma ou da escola, dependendo do modelo
        # Assumindo que a capacidade é por turma (institution_id = turma_id)
        capacidade_info = await session.get(Capacity, turma_id)
        if capacidade_info and data.capacidade < capacidade_info.capacity_used:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A capacidade total ({data.capacidade}) não pode ser inferior ao número de vagas já utilizadas ({capacidade_info.capacity_used}).",
            )

    # Atualiza o modelo com os dados do Pydantic
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(turma, key, value)

    session.add(turma)
    await session.commit()
    await session.refresh(turma)
    return TurmaResponse.from_orm(turma)

@router.get("/", response_model=list[TurmaResponse])
async def listar_turmas(
    # ... (implementação existente mantida)
    escola_id: UUID | None = Query(None),
    ativa: bool | None = None,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    stmt = select(TurmaModel)
    if escola_id is not None:
        stmt = stmt.where(TurmaModel.escola_id == escola_id)
    if ativa is not None:
        stmt = stmt.where(TurmaModel.ativa == ativa)
    rows = (await session.execute(stmt)).scalars().all()
    return [TurmaResponse.from_orm(row) for row in rows]


@router.get("/{turma_id}", response_model=TurmaResponse)
async def obter_turma(
    # ... (implementação existente mantida)
    turma_id: UUID,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    turma = await session.get(TurmaModel, turma_id)
    if not turma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turma nao encontrada")
    return TurmaResponse.from_orm(turma)
