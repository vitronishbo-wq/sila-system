from __future__ import annotations
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sa_update
from app.modules.economy.taxpayer.application.ports.taxpayer_repository import TaxpayerRepositoryPort
from app.modules.economy.taxpayer.infrastructure.models.taxpayer_model import TaxpayerModel
from app.modules.economy.taxpayer.domain.entities.taxpayer import Taxpayer

class SQLAlchemyTaxpayerRepository(TaxpayerRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity: Taxpayer) -> Taxpayer:
        model = TaxpayerModel(id=entity.id, tenant_id=entity.tenant_id, citizen_id=entity.citizen_id, nif=entity.nif, name=entity.name, status=entity.status.value, version=entity.version, created_at=entity.created_at, updated_at=entity.updated_at)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return _to_entity(model)

    async def get(self, id: UUID) -> Optional[Taxpayer]:
        q = await self.session.execute(select(TaxpayerModel).where(TaxpayerModel.id == id))
        model = q.scalars().first()
        return _to_entity(model) if model else None

    async def get_by_nif(self, nif: str) -> Optional[Taxpayer]:
        q = await self.session.execute(select(TaxpayerModel).where(TaxpayerModel.nif == nif))
        model = q.scalars().first()
        return _to_entity(model) if model else None

    async def list(self, limit: int=100, offset: int=0) -> List[Taxpayer]:
        q = await self.session.execute(select(TaxpayerModel).limit(limit).offset(offset))
        models = q.scalars().all()
        return [_to_entity(m) for m in models]

    async def update(self, entity: Taxpayer) -> Taxpayer:
        await self.session.execute(sa_update(TaxpayerModel).where(TaxpayerModel.id == entity.id).values(name=entity.name, nif=entity.nif, status=entity.status.value, version=entity.version, updated_at=entity.updated_at))
        await self.session.flush()
        q = await self.session.execute(select(TaxpayerModel).where(TaxpayerModel.id == entity.id))
        model = q.scalars().first()
        return _to_entity(model)

    async def delete(self, id: UUID) -> None:
        q = await self.session.execute(select(TaxpayerModel).where(TaxpayerModel.id == id))
        model = q.scalars().first()
        if model:
            await self.session.delete(model)
            await self.session.flush()

def _to_entity(model: TaxpayerModel) -> Taxpayer:
    return Taxpayer(id=model.id, tenant_id=model.tenant_id, citizen_id=model.citizen_id, nif=model.nif, name=model.name, status=__import__('app.modules.economy.taxpayer.domain.enums.taxpayer_status', fromlist=['TaxpayerStatus']).TaxpayerStatus(model.status), created_at=model.created_at, updated_at=model.updated_at, version=model.version)