from __future__ import annotations
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.modules.taxpayer.infrastructure.repositories.sqlalchemy_taxpayer_repository import (
    SQLAlchemyTaxpayerRepository,
)
from app.modules.taxpayer.domain.entities.taxpayer import Taxpayer as TaxpayerEntity
from app.modules.taxpayer.api import schemas

router = APIRouter()


def _to_entity(payload: schemas.TaxpayerCreate) -> TaxpayerEntity:
    # Build domain entity from create payload
    return TaxpayerEntity(
        tenant_id=payload.tenant_id,
        citizen_id=payload.citizen_id,
        nif=payload.nif,
        name=payload.name,
    )


@router.post("/taxpayers", response_model=schemas.TaxpayerRead, status_code=status.HTTP_201_CREATED)
async def create_taxpayer(payload: schemas.TaxpayerCreate, db=Depends(get_db)):
    repo = SQLAlchemyTaxpayerRepository(db)
    # Prevent duplicate nif
    existing = await repo.get_by_nif(payload.nif)
    if existing:
        raise HTTPException(status_code=409, detail="Taxpayer with this NIF already exists")
    entity = _to_entity(payload)
    created = await repo.add(entity)
    return created


@router.get("/taxpayers/{taxpayer_id}", response_model=schemas.TaxpayerRead)
async def get_taxpayer(taxpayer_id: UUID, db=Depends(get_db)):
    repo = SQLAlchemyTaxpayerRepository(db)
    taxpayer = await repo.get(taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    return taxpayer


@router.get("/taxpayers", response_model=List[schemas.TaxpayerRead])
async def list_taxpayers(limit: int = 100, offset: int = 0, db=Depends(get_db)):
    repo = SQLAlchemyTaxpayerRepository(db)
    items = await repo.list(limit=limit, offset=offset)
    return items


@router.put("/taxpayers/{taxpayer_id}", response_model=schemas.TaxpayerRead)
async def update_taxpayer(taxpayer_id: UUID, payload: schemas.TaxpayerUpdate, db=Depends(get_db)):
    repo = SQLAlchemyTaxpayerRepository(db)
    taxpayer = await repo.get(taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    # apply updates
    taxpayer.update_data(name=payload.name, nif=payload.nif)
    updated = await repo.update(taxpayer)
    return updated


@router.delete("/taxpayers/{taxpayer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_taxpayer(taxpayer_id: UUID, db=Depends(get_db)):
    repo = SQLAlchemyTaxpayerRepository(db)
    taxpayer = await repo.get(taxpayer_id)
    if not taxpayer:
        raise HTTPException(status_code=404, detail="Taxpayer not found")
    await repo.delete(taxpayer_id)
    return None
