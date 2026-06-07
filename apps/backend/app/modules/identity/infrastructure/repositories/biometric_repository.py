from __future__ import annotations

from sqlalchemy import select

from apps.backend.app.core.database.repositories.base_repository import BaseRepository
from apps.backend.app.modules.identity.infrastructure.models.biometric_model import (
    IdentityBiometric,
)


class BiometricRepository(BaseRepository):
    """Async repository for identity biometrics."""

    async def create(self, biometric: IdentityBiometric) -> IdentityBiometric:
        await self.add(biometric)
        await self.session.flush()
        return biometric

    async def get_by_id(self, biometric_id: str) -> IdentityBiometric | None:
        return await self.get(IdentityBiometric, biometric_id)

    async def list_by_citizen(
        self,
        citizen_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[IdentityBiometric]:
        result = await self.session.execute(
            select(IdentityBiometric)
            .where(IdentityBiometric.citizen_id == citizen_id)
            .order_by(IdentityBiometric.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def list_by_type(
        self,
        citizen_id: str,
        biometric_type: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[IdentityBiometric]:
        result = await self.session.execute(
            select(IdentityBiometric)
            .where(
                IdentityBiometric.citizen_id == citizen_id,
                IdentityBiometric.biometric_type == biometric_type,
            )
            .order_by(IdentityBiometric.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def update_status(self, biometric_id: str, status: str) -> IdentityBiometric | None:
        biometric = await self.get_by_id(biometric_id)
        if not biometric:
            return None
        biometric.status = status
        await self.session.flush()
        return biometric


__all__ = ["BiometricRepository"]
