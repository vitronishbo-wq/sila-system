from datetime import datetime
from typing import Any

from sqlalchemy.future import select

from apps.backend.app.domain.database.session import AsyncSessionLocal
from ..models.user_model import UserModel


class UserRepository:
    """Async repository for User persistence"""

    def __init__(self, db: Any = None):
        self.db = db

    async def create(self, user):
        """Create and persist new user"""
        if self.db is not None:
            await self.db.users.insert_one(user)
            return user
        async with AsyncSessionLocal() as session:
            model = self._to_model(user)
            session.add(model)
            await session.commit()
            return model

    def _to_model(self, user):
        if isinstance(user, dict):
            citizen_id = user.get("citizen_id")
            email = user.get("email")
            if not email and citizen_id:
                email = f"{citizen_id}@identity.local"
            if not email:
                raise ValueError("email is required when using SQLAlchemy persistence")
            active = user.get("active")
            if active is None:
                status = user.get("status")
                active = status is None or status == "ACTIVE"
            return UserModel(
                id=user.get("id"),
                citizen_id=citizen_id,
                email=email,
                active=active,
                created_at=user.get("created_at") or datetime.utcnow(),
            )
        return UserModel(
            id=user.id,
            citizen_id=user.citizen_id,
            email=user.email,
            active=getattr(user, "active", True),
            created_at=getattr(user, "created_at", datetime.utcnow()),
        )

    async def find_by_email(self, email):
        """Find user by email"""
        async with AsyncSessionLocal() as session:
            query = select(UserModel).where(
                UserModel.email == email
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def find_by_citizen_id(self, citizen_id):
        """Find user by citizen_id"""
        async with AsyncSessionLocal() as session:
            query = select(UserModel).where(
                UserModel.citizen_id == citizen_id
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_by_identity(self, identity_id):
        if self.db is not None:
            return await self.db.users.find_one(
                {"identity_id": identity_id}
            )
        if not hasattr(UserModel, "identity_id"):
            return None
        async with AsyncSessionLocal() as session:
            query = select(UserModel).where(
                UserModel.identity_id == identity_id
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
