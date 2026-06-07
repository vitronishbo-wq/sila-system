from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.procurement.domain.models.bid import Bid
from apps.backend.app.modules.procurement.domain.ports.bid_repository_port import BidRepositoryPort
from apps.backend.app.modules.procurement.infrastructure.orm.bid_model import BidModel


class SQLAlchemyBidRepository(BidRepositoryPort):
    """Adapter: SQLAlchemy implementation of BidRepositoryPort."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, bid: Bid) -> Bid:
        """Create a new bid."""
        model = BidModel.from_domain(bid)
        self.session.add(model)
        await self.session.flush()
        return model.to_domain()

    async def save(self, bid: Bid) -> Bid:
        """Save/update a bid."""
        model = BidModel.from_domain(bid)
        await self.session.merge(model)
        await self.session.flush()
        return bid

    async def get_by_id(self, bid_id: str) -> Bid | None:
        """Get bid by ID."""
        stmt = select(BidModel).where(BidModel.id == bid_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def list_by_tender(self, tender_id: str, limit: int = 100, offset: int = 0) -> list[Bid]:
        """List bids for a tender."""
        stmt = select(BidModel).where(BidModel.tender_id == tender_id).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_by_supplier(
        self, supplier_id: str, limit: int = 100, offset: int = 0
    ) -> list[Bid]:
        """List bids from a supplier."""
        stmt = (
            select(BidModel).where(BidModel.supplier_id == supplier_id).limit(limit).offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_by_status(self, status: str, limit: int = 100, offset: int = 0) -> list[Bid]:
        """List bids by status."""
        stmt = select(BidModel).where(BidModel.status == status).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Bid]:
        """List all bids."""
        stmt = select(BidModel).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def delete(self, bid_id: str) -> bool:
        """Delete a bid."""
        stmt = select(BidModel).where(BidModel.id == bid_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
