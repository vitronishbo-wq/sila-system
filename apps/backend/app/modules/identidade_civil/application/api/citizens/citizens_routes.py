"""
Rotas de Cidadãos - Módulo Identidade Civil

REFATORADO: Agora usa CitizenRepository para operações locais
e delega consultas biográficas ao FUC via CitizenQueryService.
"""
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.iam.models.user import User
from app.core.helpers import safe_get, safe_isoformat
from app.modules.identidade_civil.infrastructure.repositories.citizen_repository import CitizenRepository
from app.modules.identidade_civil.exceptions import NotFoundException, BusinessRuleException

router = APIRouter(prefix="/citizens", tags=["Citizens"])


# Schemas
class CitizenResponse(BaseModel):
    citizen_id: str
    document_number: Optional[str]
    full_name: str
    birth_date: Optional[date]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    model_config = ConfigDict(from_attributes=True)


def get_citizen_repo(db: AsyncSession = Depends(get_db)) -> CitizenRepository:
    """Provedor de dependência para CitizenRepository."""
    return CitizenRepository(db)


# Endpoints (apenas leitura - escrita deve ir via FUC)
@router.get("/", response_model=List[CitizenResponse])
async def list_citizens(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    repo: CitizenRepository = Depends(get_citizen_repo)
):
    """Lista cidadãos do cache local com paginação."""
    citizens = await repo.list_all(limit=limit, offset=skip)
    return [
        CitizenResponse(
            citizen_id=str(c.citizen_id),
            document_number=safe_get(c, "document_number"),
            full_name=c.full_name,
            birth_date=safe_get(c, "birth_date"),
            gender=safe_get(c, "gender"),
            phone=safe_get(c, "phone"),
            email=safe_get(c, "email")
        )
        for c in citizens
    ]


@router.get("/search", response_model=List[CitizenResponse])
async def search_citizens(
    q: str = Query(..., min_length=2, description="Pesquisar por nome"),
    current_user: User = Depends(get_current_user),
    repo: CitizenRepository = Depends(get_citizen_repo)
):
    """Pesquisa cidadãos por nome."""
    citizens = await repo.search_by_name(q)
    return [
        CitizenResponse(
            citizen_id=str(c.citizen_id),
            document_number=safe_get(c, "document_number"),
            full_name=c.full_name,
            birth_date=safe_get(c, "birth_date"),
            gender=safe_get(c, "gender"),
            phone=safe_get(c, "phone"),
            email=safe_get(c, "email")
        )
        for c in citizens
    ]


@router.get("/{citizen_id}")
async def get_citizen(
    citizen_id: str,
    current_user: User = Depends(get_current_user),
    repo: CitizenRepository = Depends(get_citizen_repo)
):
    """Obtém detalhes de um cidadão."""
    from uuid import UUID
    try:
        cid = UUID(citizen_id)
    except ValueError:
        raise BusinessRuleException("ID de cidadão inválido")

    citizen = await repo.get_by_id(cid)
    if not citizen:
        raise NotFoundException("Cidadão não encontrado")

    return {
        "citizen_id": str(citizen.citizen_id),
        "document_number": safe_get(citizen, "document_number"),
        "full_name": citizen.full_name,
        "birth_date": safe_isoformat(safe_get(citizen, "birth_date")),
        "gender": safe_get(citizen, "gender"),
        "phone": safe_get(citizen, "phone"),
        "email": safe_get(citizen, "email"),
        "nif": safe_get(citizen, "nif"),
        "province_id": str(safe_get(citizen, "province_id")) if safe_get(citizen, "province_id") else None,
        "municipality_id": str(safe_get(citizen, "municipality_id")) if safe_get(citizen, "municipality_id") else None,
        "current_address": safe_get(citizen, "current_address"),
        "vital_status": safe_get(citizen, "vital_status"),
        "created_at": safe_isoformat(safe_get(citizen, "created_at")),
        "updated_at": safe_isoformat(safe_get(citizen, "updated_at"))
    }


# NOTA: Endpoints de CREATE/UPDATE removidos.
# Criação/alteração de cidadãos deve ser feita via módulo FUC (Single Source of Truth).
