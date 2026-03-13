import pytest
from tests.factories.user_factory import UserFactory
from modules.identity.models.user import User

def test_factory_build():
    """Test building a user without DB"""
    u = UserFactory.build()
    assert u.email
    assert isinstance(u, User)

@pytest.mark.asyncio
async def test_factory_db(db):
    """Test saving a user to DB"""
    try:
        u = UserFactory.build()
        db.add(u)
        await db.commit()
        await db.refresh(u)
        assert u.id
    except Exception as e:
        print(f"\n\nCRITICAL_DB_ERROR: {e}\n\n")
        raise e
