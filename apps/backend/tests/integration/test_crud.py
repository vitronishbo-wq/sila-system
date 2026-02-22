import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.crud import crud_user
from app.database import Base, engine
from app.models import User


@pytest.mark.asyncio
class TestCRUD:

    @pytest.fixture(scope="module")
    async def test_db(self):
                async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session() as session:
            yield session

    async def test_create_user(self, test_db: AsyncSession):
        # Example test for creating a user
        new_user = User(username="testuser", hashed_password=settings.PASSWORD)
        await crud_user.create(test_db, obj_in=new_user)
        await test_db.commit()

        user = await crud_user.get_by_username(test_db, username="testuser")
        assert user is not None
        assert user.username == "testuser"

    async def test_update_user(self, test_db: AsyncSession):
        # Example test for updating a user
        user = await crud_user.get_by_username(test_db, username="testuser")
        user.username = "updateduser"
        await test_db.commit()

        updated_user = await crud_user.get_by_username(test_db, username="updateduser")
        assert updated_user is not None
        assert updated_user.username == "updateduser"

    async def test_delete_user(self, test_db: AsyncSession):
        # Example test for deleting a user
        user = await crud_user.get_by_username(test_db, username="updateduser")
        await crud_user.remove(test_db, id=user.id)
        await test_db.commit()

        deleted_user = await crud_user.get_by_username(test_db, username="updateduser")
        assert deleted_user is None
