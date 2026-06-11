from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.api.schemas.escola_schema import EscolaCreate, EscolaResponse
from apps.backend.app.modules.educacao.domain.models import CicloEnsino, TipoEscola
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access

router = APIRouter(prefix="/escolas", tags=["Educacao - Escolas"])


@router.post("/", response_model=EscolaResponse, status_code=status.HTTP_201_CREATED)
async def criar_escola(
    data: EscolaCreate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    escola = EscolaModel(
        codigo_med=data.codigo_med,
        nome=data.nome,
        tipo=data.tipo,
        ciclos=[c.value for c in data.ciclos],
        provincia=data.provincia,
        municipio=data.municipio,
        comuna=data.comuna,
        bairro=data.bairro,
        endereco=data.endereco,
        contacto=data.contacto,
        email=data.email,
        ativa=True,
    )
    session.add(escola)
    await session.flush()
    await session.refresh(escola)
    await session.commit()
    return EscolaResponse(
        id=escola.id,
        codigo_med=escola.codigo_med,
        nome=escola.nome,
        tipo=escola.tipo,
        ciclos=escola.ciclos,
        provincia=escola.provincia,
        municipio=escola.municipio,
        comuna=escola.comuna,
        bairro=escola.bairro,
        endereco=escola.endereco,
        contacto=escola.contacto,
        email=escola.email,
        ativa=escola.ativa,
    )


@router.get("/", response_model=list[EscolaResponse])
async def listar_escolas(
    provincia: str | None = Query(None, max_length=128),
    municipio: str | None = Query(None, max_length=128),
    tipo: TipoEscola | None = None,
    ativa: bool | None = None,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    from sqlalchemy import select

    stmt = select(EscolaModel)
    if provincia is not None:
        stmt = stmt.where(EscolaModel.provincia == provincia)
    if municipio is not None:
        stmt = stmt.where(EscolaModel.municipio == municipio)
    if tipo is not None:
        stmt = stmt.where(EscolaModel.tipo == tipo.value)
    if ativa is not None:
        stmt = stmt.where(EscolaModel.ativa == ativa)

    rows = (await session.execute(stmt)).scalars().all()
    return [
        EscolaResponse(
            id=row.id,
            codigo_med=row.codigo_med,
            nome=row.nome,
            tipo=row.tipo,
            ciclos=row.ciclos,
            provincia=row.provincia,
            municipio=row.municipio,
            comuna=row.comuna,
            bairro=row.bairro,
            endereco=row.endereco,
            contacto=row.contacto,
            email=row.email,
            ativa=row.ativa,
        )
        for row in rows
    ]


@router.get("/{escola_id}", response_model=EscolaResponse)
async def obter_escola(
    escola_id: UUID,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    escola = await session.get(EscolaModel, escola_id)
    if not escola:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Escola nao encontrada")
    return EscolaResponse(
        id=escola.id,
        codigo_med=escola.codigo_med,
        nome=escola.nome,
        tipo=escola.tipo,
        ciclos=escola.ciclos,
        provincia=escola.provincia,
        municipio=escola.municipio,
        comuna=escola.comuna,
        bairro=escola.bairro,
        endereco=escola.endereco,
        contacto=escola.contacto,
        email=escola.email,
        ativa=escola.ativa,
    )
