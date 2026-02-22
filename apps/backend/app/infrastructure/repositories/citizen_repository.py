from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ...domain.citizen import Citizen
from ...application.ports.citizen_repository_port import CitizenRepositoryPort
from ..models.citizen_model import CitizenModel

class CitizenRepository(CitizenRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, citizen: Citizen) -> Citizen:
        # Conversão de domínio para modelo infra
        model = CitizenModel(**citizen.__dict__)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return Citizen(**model.__dict__)

    async def update(self, citizen: Citizen) -> Citizen:
        result = await self.session.execute(select(CitizenModel).where(CitizenModel.id == citizen.id))
        model = result.scalar_one()
        for key, value in citizen.__dict__.items():
            setattr(model, key, value)
        await self.session.commit()
        await self.session.refresh(model)
        return Citizen(**model.__dict__)

    async def get_by_id(self, id: UUID) -> Optional[Citizen]:
        result = await self.session.execute(select(CitizenModel).where(CitizenModel.id == id))
        model = result.scalar_one_or_none()
        return Citizen(**model.__dict__) if model else None

    async def get_by_national_id_number(self, national_id_number: str) -> Optional[Citizen]:
        result = await self.session.execute(select(CitizenModel).where(CitizenModel.national_id_number == national_id_number))
        model = result.scalar_one_or_none()
        return Citizen(**model.__dict__) if model else None

    async def get_by_nif(self, nif: str) -> Optional[Citizen]:
        result = await self.session.execute(select(CitizenModel).where(CitizenModel.nif == nif))
        model = result.scalar_one_or_none()
        return Citizen(**model.__dict__) if model else None

    async def list(self, *, filters: dict, limit: int, offset: int) -> List[Citizen]:
        query = select(CitizenModel)
        # Filtros dinâmicos
        for attr, value in filters.items():
            if value is not None:
                query = query.where(getattr(CitizenModel, attr) == value)
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [Citizen(**row.__dict__) for row in result.scalars().all()]

    async def soft_delete(self, id: UUID) -> None:
        result = await self.session.execute(select(CitizenModel).where(CitizenModel.id == id))
        model = result.scalar_one()
        model.status = 'INACTIVE'
        await self.session.commit()
