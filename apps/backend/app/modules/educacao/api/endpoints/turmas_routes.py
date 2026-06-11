from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.api.schemas.turma_schema import TurmaCreate, TurmaResponse
from apps.backend.app.modules.educacao.infrastructure.models.turma_model import TurmaModel
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access

router = APIRouter(prefix="/turmas", tags=["Educacao - Turmas"])


@router.post("/", response_model=TurmaResponse, status_code=status.HTTP_201_CREATED)
async def criar_turma(
    data: TurmaCreate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
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
    return TurmaResponse(
        id=turma.id,
        escola_id=turma.escola_id,
        ano_letivo_id=turma.ano_letivo_id,
        codigo=turma.codigo,
        classe=turma.classe,
        turno=turma.turno,
        capacidade=turma.capacidade,
        ativa=turma.ativa,
        territory_id=turma.territory_id,
        created_by=turma.created_by,
        managed_by=turma.managed_by,
    )


@router.get("/", response_model=list[TurmaResponse])
async def listar_turmas(
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
    return [
        TurmaResponse(
            id=row.id,
            escola_id=row.escola_id,
            ano_letivo_id=row.ano_letivo_id,
            codigo=row.codigo,
            classe=row.classe,
            turno=row.turno,
            capacidade=row.capacidade,
            ativa=row.ativa,
            territory_id=row.territory_id,
            created_by=row.created_by,
            managed_by=row.managed_by,
        )
        for row in rows
    ]


@router.get("/{turma_id}", response_model=TurmaResponse)
async def obter_turma(
    turma_id: UUID,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    turma = await session.get(TurmaModel, turma_id)
    if not turma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turma nao encontrada")
    return TurmaResponse(
        id=turma.id,
        escola_id=turma.escola_id,
        ano_letivo_id=turma.ano_letivo_id,
        codigo=turma.codigo,
        classe=turma.classe,
        turno=turma.turno,
        capacidade=turma.capacidade,
        ativa=turma.ativa,
        territory_id=turma.territory_id,
        created_by=turma.created_by,
        managed_by=turma.managed_by,
    )
