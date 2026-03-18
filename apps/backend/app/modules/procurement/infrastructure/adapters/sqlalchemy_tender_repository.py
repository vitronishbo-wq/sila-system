from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from apps.backend.app.modules.procurement.domain.models.tender import Tender
from apps.backend.app.modules.procurement.domain.ports.tender_repository_port import TenderRepositoryPort
from apps.backend.app.modules.procurement.infrastructure.orm.tender_model import TenderModel

class SQLAlchemyTenderRepository(TenderRepositoryPort):
    """Adapter: SQLAlchemy implementation of TenderRepositoryPort."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tender: Tender) -> Tender:
        """Create a new tender."""
        model = TenderModel.from_domain(tender)
        self.session.add(model)
        await self.session.flush()
        return model.to_domain()

    async def save(self, tender: Tender) -> Tender:
        """Save/update a tender."""
        model = TenderModel.from_domain(tender)
        await self.session.merge(model)
        await self.session.flush()
        return tender

    async def get_by_id(self, tender_id: str) -> Optional[Tender]:
        """Get tender by ID."""
        stmt = select(TenderModel).where(TenderModel.id == tender_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def list_by_status(self, status: str, limit: int=100, offset: int=0) -> List[Tender]:
        """List tenders by status."""
        stmt = select(TenderModel).where(TenderModel.status == status).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_all(self, limit: int=100, offset: int=0) -> List[Tender]:
        """List all tenders."""
        stmt = select(TenderModel).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def delete(self, tender_id: str) -> bool:
        """Delete a tender."""
        stmt = select(TenderModel).where(TenderModel.id == tender_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False