from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.bridges.citizen_repository_bridge import CitizenRepository

from ...application.citizen_service import CitizenService
from ...infrastructure.db.session import get_session
from ..schemas.citizen_schema import CitizenCreateSchema, CitizenReadSchema, CitizenUpdateSchema

router = APIRouter(prefix="/citizens", tags=["citizens"])

session_dep = Depends(get_session)
name_query = Query(None)
bi_query = Query(None)
nif_query = Query(None)
phone_query = Query(None)
province_query = Query(None)
birth_date_query = Query(None)
status_query = Query(None)
limit_query = Query(10, ge=1, le=100)
offset_query = Query(0, ge=0)


async def get_citizen_service(session: AsyncSession = session_dep):
    repo = CitizenRepository(session)
    return CitizenService(repo)

citizen_service_dep = Depends(get_citizen_service)


@router.post("/", response_model=CitizenReadSchema)
async def create_citizen(
    citizen_in: CitizenCreateSchema, service: CitizenService = citizen_service_dep
):
    citizen = await service.create_citizen(citizen_in)
    return citizen


@router.patch("/{citizen_id}", response_model=CitizenReadSchema)
async def update_citizen(
    citizen_id: UUID,
    citizen_in: CitizenUpdateSchema,
    service: CitizenService = citizen_service_dep,
):
    citizen = await service.get_citizen_by_id(citizen_id)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    for field, value in citizen_in.dict(exclude_unset=True).items():
        setattr(citizen, field, value)
    updated = await service.update_citizen(citizen)
    return updated


@router.get("/{citizen_id}", response_model=CitizenReadSchema)
async def get_citizen_by_id(
    citizen_id: UUID, service: CitizenService = citizen_service_dep
):
    citizen = await service.get_citizen_by_id(citizen_id)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return citizen


@router.get("/by_bi/{bi}", response_model=CitizenReadSchema)
async def get_citizen_by_bi(bi: str, service: CitizenService = citizen_service_dep):
    citizen = await service.get_citizen_by_national_id_number(bi)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return citizen


@router.get("/by_nif/{nif}", response_model=CitizenReadSchema)
async def get_citizen_by_nif(nif: str, service: CitizenService = citizen_service_dep):
    citizen = await service.get_citizen_by_nif(nif)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return citizen


@router.get("/", response_model=list[CitizenReadSchema])
async def list_citizens(
    name: str | None = name_query,
    bi: str | None = bi_query,
    nif: str | None = nif_query,
    phone: str | None = phone_query,
    province: str | None = province_query,
    birth_date: str | None = birth_date_query,
    status: str | None = status_query,
    limit: int = limit_query,
    offset: int = offset_query,
    service: CitizenService = citizen_service_dep,
):
    filters = {
        "full_name": name,
        "national_id_number": bi,
        "nif": nif,
        "phone": phone,
        "province": province,
        "birth_date": birth_date,
        "status": status,
    }
    citizens = await service.list_citizens(filters=filters, limit=limit, offset=offset)
    return citizens


@router.delete("/{citizen_id}")
async def soft_delete_citizen(
    citizen_id: UUID, service: CitizenService = citizen_service_dep
):
    await service.soft_delete_citizen(citizen_id)
    return {"detail": "Citizen soft deleted (status set to INACTIVE)"}
