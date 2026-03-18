from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from apps.backend.app.modules.procurement.domain.models.contract import Contract
from apps.backend.app.modules.procurement.domain.ports.contract_repository_port import ContractRepositoryPort
from apps.backend.app.modules.procurement.infrastructure.orm.contract_model import ContractModel

class SQLAlchemyContractRepository(ContractRepositoryPort):
    """Adapter: SQLAlchemy implementation of ContractRepositoryPort."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, contract: Contract) -> Contract:
        """Create a new contract."""
        model = ContractModel.from_domain(contract)
        self.session.add(model)
        await self.session.flush()
        return model.to_domain()

    async def save(self, contract: Contract) -> Contract:
        """Save/update a contract."""
        model = ContractModel.from_domain(contract)
        await self.session.merge(model)
        await self.session.flush()
        return contract

    async def get_by_id(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID."""
        stmt = select(ContractModel).where(ContractModel.id == contract_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def list_by_status(self, status: str, limit: int=100, offset: int=0) -> List[Contract]:
        """List contracts by status."""
        stmt = select(ContractModel).where(ContractModel.status == status).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_all(self, limit: int=100, offset: int=0) -> List[Contract]:
        """List all contracts."""
        stmt = select(ContractModel).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def delete(self, contract_id: str) -> bool:
        """Delete a contract."""
        stmt = select(ContractModel).where(ContractModel.id == contract_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False