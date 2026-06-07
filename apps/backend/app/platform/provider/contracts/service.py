import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from apps.backend.app.core.db import db
from apps.backend.app.platform.provider.contracts.models import ProviderContract
from sqlalchemy import select

logger = logging.getLogger(__name__)


class ContractStatus(str, Enum):
    DRAFT = "draft"
    TESTING = "testing"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class ContractService:
    async def get(self, provider: str) -> Optional[ProviderContract]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderContract).where(
                    ProviderContract.provider == provider
                ).order_by(ProviderContract.created_at.desc()).limit(1)
            )
            return result.scalar_one_or_none()

    async def get_all(self) -> list[ProviderContract]:
        async with db.session_factory() as session:
            result = await session.execute(
                select(ProviderContract).order_by(ProviderContract.provider)
            )
            return list(result.scalars().all())

    async def register(
        self,
        provider: str,
        contract_number: str,
        entity: str,
        status: ContractStatus = ContractStatus.DRAFT,
        signed_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None,
        terms: Optional[str] = None,
    ) -> ProviderContract:
        async with db.session_factory() as session:
            contract = ProviderContract(
                provider=provider,
                contract_number=contract_number,
                entity=entity,
                status=status.value,
                signed_at=signed_at,
                expires_at=expires_at,
                terms=terms,
            )
            session.add(contract)
            await session.commit()
            await session.refresh(contract)
            logger.info(f"contract provider={provider} number={contract_number} status={status.value}")
            return contract

    async def to_dict(self, provider: str) -> dict:
        contract = await self.get(provider)
        if not contract:
            return {"provider": provider, "status": "missing"}
        return {
            "provider": contract.provider,
            "contract_number": contract.contract_number,
            "entity": contract.entity,
            "signed_at": contract.signed_at.isoformat() if contract.signed_at else None,
            "expires_at": contract.expires_at.isoformat() if contract.expires_at else None,
            "status": contract.status,
            "terms": contract.terms,
        }
