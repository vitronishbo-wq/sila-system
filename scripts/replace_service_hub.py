#!/usr/bin/env python3
import os
from pathlib import Path

# -----------------------------
# Paths do projeto
# -----------------------------
BASE_DIR = Path(__file__).parent.parent / "apps" / "backend" / "modules" / "service_hub"
ENDPOINTS_DIR = BASE_DIR / "endpoints"
SCHEMAS_DIR = BASE_DIR / "schemas"

# -----------------------------
# Certificar pastas existem
# -----------------------------
ENDPOINTS_DIR.mkdir(parents=True, exist_ok=True)
SCHEMAS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Conteúdos dos arquivos
# -----------------------------

# crud.py
CRUD_CONTENT = """\
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Service
from .schemas.service_hub_crud import ServiceCreate, ServiceUpdate

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit).order_by(self.model.id))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict(exclude_unset=True))
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.id == id))
        obj = result.scalar_one()
        await db.delete(obj)
        await db.commit()
        return obj

class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Service]:
        result = await db.execute(select(Service).where(Service.name == name))
        return result.scalar_one_or_none()

def get_service_crud() -> CRUDService:
    return CRUDService(Service)
"""

# service_hub_service.py
SERVICE_HUB_SERVICE_CONTENT = """\
from .crud import CRUDService, get_service_crud
from sqlalchemy.ext.asyncio import AsyncSession

class ServiceHubService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.crud = get_service_crud()

    async def list_services(self, skip: int = 0, limit: int = 100):
        return await self.crud.get_multi(self.db, skip=skip, limit=limit)

    async def create_service(self, service_in):
        return await self.crud.create(self.db, obj_in=service_in)

    async def update_service(self, service_id: int, service_in):
        db_obj = await self.crud.get(self.db, service_id)
        if not db_obj:
            return None
        return await self.crud.update(self.db, db_obj=db_obj, obj_in=service_in)
"""

# schemas/service_hub_crud.py
SCHEMAS_CONTENT = """\
from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    description: str | None = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(ServiceBase):
    pass
"""

# endpoints/router.py
ROUTER_CONTENT = """\
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.database import get_db
from apps.backend.app.modules.service_hub.crud import get_service_crud
from apps.backend.app.modules.service_hub.schemas.service_hub_crud import ServiceCreate, ServiceUpdate

router = APIRouter(prefix="/service_hub", tags=["Service Hub"])

@router.get("/services")
async def list_services(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    crud = get_service_crud()
    return await crud.get_multi(db, skip=skip, limit=limit)

@router.post("/services")
async def create_service(service_in: ServiceCreate, db: AsyncSession = Depends(get_db)):
    crud = get_service_crud()
    return await crud.create(db, obj_in=service_in)

@router.put("/services/{service_id}")
async def update_service(service_id: int, service_in: ServiceUpdate, db: AsyncSession = Depends(get_db)):
    crud = get_service_crud()
    db_obj = await crud.get(db, service_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Service not found")
    return await crud.update(db, db_obj=db_obj, obj_in=service_in)
"""


# -----------------------------
# Função para gravar arquivos
# -----------------------------
def write_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    print(f"✅ {path} gravado com sucesso.")


# -----------------------------
# Substituir/criar arquivos
# -----------------------------
write_file(BASE_DIR / "crud.py", CRUD_CONTENT)
write_file(BASE_DIR / "service_hub_service.py", SERVICE_HUB_SERVICE_CONTENT)
write_file(SCHEMAS_DIR / "service_hub_crud.py", SCHEMAS_CONTENT)
write_file(ENDPOINTS_DIR / "router.py", ROUTER_CONTENT)

print("\n🎉 Todos os arquivos do Service Hub foram substituídos/criados com sucesso.")
