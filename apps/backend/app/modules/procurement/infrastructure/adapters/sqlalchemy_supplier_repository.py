from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.procurement.domain.models.supplier import Supplier
from apps.backend.app.modules.procurement.domain.ports.supplier_repository_port import (
    SupplierRepositoryPort,
)
from apps.backend.app.modules.procurement.infrastructure.orm.supplier_model import SupplierModel


class SQLAlchemySupplierRepository(SupplierRepositoryPort):
    """Adapter: SQLAlchemy implementation of SupplierRepositoryPort."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, supplier: Supplier) -> Supplier:
        """Create a new supplier."""
        model = SupplierModel.from_domain(supplier)
        self.session.add(model)
        await self.session.flush()
        return model.to_domain()

    async def save(self, supplier: Supplier) -> Supplier:
        """Save/update a supplier."""
        model = SupplierModel.from_domain(supplier)
        await self.session.merge(model)
        await self.session.flush()
        return supplier

    async def get_by_id(self, supplier_id: str) -> Supplier | None:
        """Get supplier by ID."""
        stmt = select(SupplierModel).where(SupplierModel.id == supplier_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def get_by_tax_id(self, tax_id: str) -> Supplier | None:
        """Get supplier by tax ID."""
        stmt = select(SupplierModel).where(SupplierModel.tax_id == tax_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def list_by_status(
        self, status: str, limit: int = 100, offset: int = 0
    ) -> list[Supplier]:
        """List suppliers by status."""
        stmt = (
            select(SupplierModel).where(SupplierModel.status == status).limit(limit).offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Supplier]:
        """List all suppliers."""
        stmt = select(SupplierModel).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def delete(self, supplier_id: str) -> bool:
        """Delete a supplier."""
        stmt = select(SupplierModel).where(SupplierModel.id == supplier_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False
