"""User repository backed by SQLAlchemy ORM."""

from typing import Optional
from uuid import UUID
from uuid import UUID as UUIDType

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from modules.auth.models.user import User, UserCreate
from modules.common.utils.utils import verify_password


class UserRepository:
    """Data-access helper for User entities."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, payload: UserCreate) -> User:
        region_uuid: Optional[UUIDType] = None
        if payload.region_id:
            try:
                region_uuid = UUID(payload.region_id)
            except (ValueError, TypeError):
                region_uuid = None

        user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=func.crypt(payload.password, func.gen_salt("bf")),
            is_active=payload.is_active,
            is_superuser=payload.is_superuser,
            level=payload.level,
            region_id=region_uuid,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def update_user(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
