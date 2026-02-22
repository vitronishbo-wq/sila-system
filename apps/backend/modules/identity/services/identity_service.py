"""
Identity Service for managing external identity provider relationships.

This service handles CRUD operations for Identity model,
enabling OAuth/SSO functionality and user identity management.
"""

from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.identity import Identity
from ..schemas.identity import IdentityCreate, IdentityRead, IdentityUpdate


class IdentityService:
    """
    Service class for Identity model operations.

    Provides methods for creating, reading, updating, and deleting
    identity provider relationships.
    """

    @staticmethod
    async def get_by_id(db: AsyncSession, identity_id: int) -> Optional[IdentityRead]:
        """Get identity by ID."""
        result = await db.execute(select(Identity).where(Identity.id == identity_id))
        identity = result.scalar_one_or_none()
        return IdentityRead.from_orm(identity) if identity else None

    @staticmethod
    async def get_by_provider_and_external_id(
        db: AsyncSession, provider: str, external_id: str
    ) -> Optional[IdentityRead]:
        """Get identity by provider and external ID."""
        result = await db.execute(
            select(Identity).where(
                and_(Identity.provider == provider, Identity.external_id == external_id)
            )
        )
        identity = result.scalar_one_or_none()
        return IdentityRead.from_orm(identity) if identity else None

    @staticmethod
    async def get_by_user_id(db: AsyncSession, user_id: int) -> List[IdentityRead]:
        """Get all identities for a specific user."""
        result = await db.execute(
            select(Identity)
            .where(Identity.user_id == user_id)
            .order_by(Identity.created_at)
        )
        identities = result.scalars().all()
        return [IdentityRead.from_orm(identity) for identity in identities]

    @staticmethod
    async def get_by_user_and_provider(
        db: AsyncSession, user_id: int, provider: str
    ) -> Optional[IdentityRead]:
        """Get identity for a user and specific provider."""
        result = await db.execute(
            select(Identity).where(
                and_(Identity.user_id == user_id, Identity.provider == provider)
            )
        )
        identity = result.scalar_one_or_none()
        return IdentityRead.from_orm(identity) if identity else None

    @staticmethod
    async def create(db: AsyncSession, identity_data: IdentityCreate) -> IdentityRead:
        """Create a new identity."""
        # Check if identity already exists
        existing = await IdentityService.get_by_provider_and_external_id(
            db, identity_data.provider, identity_data.external_id
        )
        if existing:
            # Update existing identity instead of creating duplicate
            return await IdentityService.update(db, existing.id, identity_data)

        identity = Identity(**identity_data.dict())
        db.add(identity)
        await db.commit()
        await db.refresh(identity)
        return IdentityRead.from_orm(identity)

    @staticmethod
    async def update(
        db: AsyncSession, identity_id: int, identity_data: IdentityUpdate
    ) -> Optional[IdentityRead]:
        """Update an existing identity."""
        result = await db.execute(select(Identity).where(Identity.id == identity_id))
        identity = result.scalar_one_or_none()

        if not identity:
            return None

        # Update fields
        for field, value in identity_data.dict(exclude_unset=True).items():
            setattr(identity, field, value)

        await db.commit()
        await db.refresh(identity)
        return IdentityRead.from_orm(identity)

    @staticmethod
    async def delete(db: AsyncSession, identity_id: int) -> bool:
        """Delete an identity."""
        result = await db.execute(select(Identity).where(Identity.id == identity_id))
        identity = result.scalar_one_or_none()

        if not identity:
            return False

        await db.delete(identity)
        await db.commit()
        return True

    @staticmethod
    async def deactivate_by_user_and_provider(
        db: AsyncSession, user_id: int, provider: str
    ) -> bool:
        """Deactivate all identities for a user and provider."""
        result = await db.execute(
            select(Identity).where(
                and_(Identity.user_id == user_id, Identity.provider == provider)
            )
        )
        identities = result.scalars().all()

        if not identities:
            return False

        for identity in identities:
            identity.is_active = False

        await db.commit()
        return True

    @staticmethod
    async def get_active_providers_for_user(
        db: AsyncSession, user_id: int
    ) -> List[str]:
        """Get list of active providers for a user."""
        result = await db.execute(
            select(Identity.provider)
            .where(and_(Identity.user_id == user_id, Identity.is_active == True))
            .distinct()
        )
        providers = result.scalars().all()
        return list(providers)
